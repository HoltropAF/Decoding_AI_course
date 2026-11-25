  function createDownloadAdapter(getViewer, requestBrowserDownload) {
    var unavailable = ["unavailable", "not_granted", "capability_disabled", "capability_removed"];
    return async function download(name, blob) {
      try {
        var viewer = getViewer();
        if (viewer) {
          try {
            await viewer.save({ filename: name, data: blob });
            return "ready";
          } catch (error) {
            if (!error || !unavailable.includes(error.code)) throw error;
          }
        }
        await requestBrowserDownload(name, blob);
        return "requested";
      } catch (error) {
        return "failed";
      }
    };
  }
