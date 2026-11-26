"""Shared Ollama adapter checks using a synthetic loopback server."""
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib.util import find_spec
import io
import json
import threading
import unittest


@unittest.skipUnless(find_spec("requests") and find_spec("ollama"), "install the optional HTTP and SDK clients")
class OllamaAdapterContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from module_01_foundations_and_privacy.exercises import test_ollama_local
        cls.exercise = test_ollama_local

    def run_case(self, backend, response, *, stream=False, status=200):
        requests_seen = []

        class Fixture(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                requests_seen.append((self.path, payload))
                content = response if isinstance(response, bytes) else json.dumps(response).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/x-ndjson" if stream else "application/json")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, *_args):
                pass

        with ThreadingHTTPServer(("127.0.0.1", 0), Fixture) as server:
            worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01})
            worker.start()
            try:
                adapter = getattr(self.exercise, f"chat_{backend}")
                output = io.StringIO()
                with redirect_stdout(output):
                    result = adapter(f"http://127.0.0.1:{server.server_port}", "fixture", "Say hello.", stream, 0.2)
            finally:
                server.shutdown()
                worker.join()

        path, request = requests_seen[0]
        self.assertEqual(len(requests_seen), 1)
        self.assertEqual(path, "/api/chat")
        self.assertEqual(request["model"], "fixture")
        self.assertEqual(request["stream"], stream)
        self.assertEqual(request["options"]["temperature"], 0.2)
        self.assertEqual([m["role"] for m in request["messages"]], ["system", "user"])
        self.assertEqual(request["messages"][-1]["content"], "Say hello.")
        return result, output.getvalue()

    @staticmethod
    def chunk(content, done=False, **fields):
        return {"model": "fixture", "message": {"role": "assistant", "content": content}, "done": done, **fields}

    @staticmethod
    def stream(*chunks):
        return b"".join(json.dumps(chunk).encode() + b"\n" for chunk in chunks)

    def test_non_streaming_response(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend):
                result, output = self.run_case(backend, self.chunk("Hello.", True, eval_count=2))
                self.assertEqual((result["done"], result["eval_count"], output), (True, 2, "Hello.\n"))

    def test_streamed_chunks_and_final_statistics(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend):
                response = self.stream(self.chunk("Hel"), self.chunk("lo."), self.chunk("", True, eval_count=2))
                result, output = self.run_case(backend, response, stream=True)
                self.assertEqual((result["done"], result["eval_count"], output), (True, 2, "Hello.\n"))

    def test_http_failure(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend), self.assertRaises(self.exercise.OllamaChatError):
                self.run_case(backend, {"error": "Fixture unavailable"}, status=503)

    def test_stream_error(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend), self.assertRaisesRegex(self.exercise.OllamaChatError, "Fixture interrupted"):
                self.run_case(backend, self.stream(self.chunk("Hel"), {"error": "Fixture interrupted"}), stream=True)

    def test_stream_missing_completion(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend), self.assertRaisesRegex(self.exercise.OllamaChatError, "before sending completion"):
                self.run_case(backend, self.stream(self.chunk("Hel")), stream=True)

    def test_malformed_json(self):
        for backend in ("requests", "sdk"):
            with self.subTest(backend=backend), self.assertRaises(self.exercise.OllamaChatError):
                self.run_case(backend, b"not JSON")


if __name__ == "__main__":
    unittest.main()
