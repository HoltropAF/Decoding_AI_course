# Decoding AI code, design and reproducibility review

Reviewed 25 November 2026 by three independent reviewers. The dashboard has a clear learning path and a lightweight offline build. The weakest area is persistence. Ordinary checklist ticks disappear after reload, a malformed progress import can overwrite saved work, and a failed save can clear an unsaved report. Fix those before adding features. The build is easy to run, but it can report success while producing a broken offline figure.

## Snapshot and scope

The target was the Decoding AI working checkout on `development` at `1ed7ab9ffd689f59a12c993820288d1e1aa3a07d`. The working tree started with four documentation edits in `CHANGELOG.md`, `course/README.md`, `docs/setup-guide.md`, and `docs/using-the-course.md`. The reviewers used the working documentation where applicable and isolated committed source and generated output for executable checks. Earlier course-content review notes were background. The findings below were gathered for this review. Scope covered the Python bundler, dashboard interactions, a sample of adapter interfaces, and the directory handoff. Live model inference and third-party integrations were outside execution coverage. [Earlier course review](course_review.md)

| Framework | Observed alignment | Scored evidence |
| --- | ---: | ---: |
| SOLID | 14/30 (46.7%) | 15/15 (100%) |
| Apple design | 22/30 (73.3%) | 15/16 (93.8%) |
| ENCORE | 17/24 (70.8%) | 12/12 (100%) |

Each framework keeps its own scale. Evidence coverage counts the rubric checks that could be scored. Browser and build checks covered selected workflows.

## SOLID architecture and functionality

The Python builder reads configuration and Markdown, derives module routes and section metadata, inlines figures, and packages the data and Markdown parser into the HTML template. Browser JavaScript handles routes, shared state, rendering and persistence inside the resulting file. The module configuration, narrow reader callbacks and pure parsing helpers give the course a useful foundation for localized changes. The most consequential coupling appears where renderers, file imports and local storage each make their own assumptions about state. [Module configuration](../course/build_dashboard.py#L63) · [Build entry point](../course/build_dashboard.py#L496) · [Reader callbacks](../course/dashboard_template.html#L1930) · [Dashboard rendering](../course/dashboard_template.html#L3384)

| Principle | Score and checks | Evidence |
| --- | --- | --- |
| Single responsibility | 2/6 (S1 1, S2 0, S3 1) | Pure build parsers coexist with a Markdown renderer that binds navigation, checklists and clipboard interactions. State policy is repeated across import, loading and rendering. [Pure parser](../course/build_dashboard.py#L220) · [Markdown renderer](../course/dashboard_template.html#L1302) · [Import](../course/dashboard_template.html#L2493) |
| Open/closed | 4/6 (O1 2, O2 1, O3 1) | Standard modules are configuration-driven. Adding a renderer kind crosses build and UI dispatch, and a specialized behavior depends on the visible label `Tracks`. [Module build](../course/build_dashboard.py#L359) · [Render dispatch](../course/dashboard_template.html#L2712) |
| Liskov substitution | 3/6 (L1 2, L2 1, L3 0) | Ollama adapters share caller and response shapes by inspection. Download implementations can signal different outcomes and the UI assumes success. No dedicated adapter or dashboard contract suite was found in the tracked tree. [Ollama exercise](../module_01_foundations_and_privacy/exercises/test_ollama_local.py#L95) · [Download code](../course/dashboard_template.html#L2733) |
| Interface segregation | 3/6 (I1 1, I2 2, I3 0) | Narrow document records and reader callbacks help. Renderers and progress actions also reach directly into shared state, including positional keys. [Document records](../course/build_dashboard.py#L309) · [Reader](../course/dashboard_template.html#L1930) · [Wrap-up](../course/dashboard_template.html#L2619) |
| Dependency inversion | 2/6 (D1 1, D2 1, D3 0) | Build composition and a centralized download helper provide useful seams. Browser storage, import decoding and position-based identity remain coupled to the UI. [Build orchestration](../course/build_dashboard.py#L496) · [Storage](../course/dashboard_template.html#L1071) · [Section linking](../course/build_dashboard.py#L482) |

**Verified in isolated Edge.** A Module 1 privacy checklist tick was checked and serialized, but appeared unchecked after reload. A Wrap-up checkbox persisted in the comparison path. A synthetic incomplete progress file replaced the prior saved progress and left Wrap-up blank. The loader restores only keys included in initial state; ordinary Markdown ticks are created lazily. The import path commits state before establishing the full shape expected by the renderers. [State load](../course/dashboard_template.html#L1071) · [Markdown ticks](../course/dashboard_template.html#L1321) · [Progress import](../course/dashboard_template.html#L2493) · [Wrap-up rendering](../course/dashboard_template.html#L2639)

**Verified in a synthetic Markdown fixture.** Exercise extraction treats a heading inside a fenced example as an actual section heading, while the section-indexing helper skips it. A separate known maintenance issue is that reordering Wrap-up checklist entries shifts saved ticks because they are keyed by position. [Section extraction](../course/build_dashboard.py#L197) · [Heading indexing](../course/build_dashboard.py#L415) · [Documented ordering constraint](../course/README.md#L89)

## Apple design and usability

The reviewer used the Apple Human Interface Guidelines as a browser design rubric. They exercised the copied dashboard through `file://` in headless Edge, including a 390 px viewport and dark appearance. The scoring covers 15 of 16 checks. Text enlargement and zoom remain unverified. A real-device Safari pass, VoiceOver, exhaustive contrast, and speech output also remain unverified. A synthetic report download was verified in scratch and contained the entered text and course version. [Apple accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) · [Motion](https://developer.apple.com/design/human-interface-guidelines/motion)

| Area | Observed score | Evidence |
| --- | ---: | --- |
| Purpose and hierarchy | 4/4 | Home gives Orientation a clear first action and exposes the seven course cards. [Home renderer](../course/dashboard_template.html#L1630) |
| Layout and density | 2/2 | Home and Dictionary fit the 390 px viewport. The zoom and enlarged-text check is unscored. |
| Familiarity and input | 3/4 | Tabs and controls make the path discoverable. Escape did not close the mobile menu in the automated keyboard run. [Menu handler](../course/dashboard_template.html#L3483) |
| Accessibility | 2/4 | Named progress controls and live messages help. Figure enlargement is click-only and the lightbox loses focus on close. [Figure handling](../course/dashboard_template.html#L1353) · [Lightbox](../course/dashboard_template.html#L1147) |
| Typography and materials | 3/4 | Shared tokens, theming and reader settings support different preferences. Default desktop scale is 75%; enlarged text needs a direct check. A sampled light-mode destructive button in Module 2 measured 2.12:1 against white. [Theme and scale](../course/dashboard_template.html#L19) · [Destructive control](../course/dashboard_template.html#L3660) |
| Feedback and recovery | 2/4 | Blank reports are caught and Dictionary no-results guidance helped the reviewer recover. A simulated quota failure cleared an unsaved report draft despite advising the reader to copy it. [Dictionary results](../course/dashboard_template.html#L3303) · [Report save](../course/dashboard_template.html#L3632) |
| Motion | 3/4 | CSS animation and confetti respect reduced motion. Several imperative scrolls still request smooth motion. [Chapter scroll](../course/dashboard_template.html#L2186) |
| Charts and analytical views | 3/4 | Instructional figures have alt text or captions, while opening a larger figure and reaching a fuller explanation remain difficult from the keyboard. [Dictionary figure](../course/dashboard_template.html#L3261) |

Normal Wrap-up checkbox and note actions worked in the sample. Storage writes elsewhere can fail silently, so successful normal saves do not establish reliable failure recovery. Verify drafts, notes and checklist state together. [State save](../course/dashboard_template.html#L1096) · [Wrap-up notes](../course/dashboard_template.html#L2660)

## ENCORE reproducibility and handoff

ENCORE was adapted to a course software repository. The deliverable is the bundled offline HTML. Chapter Markdown, slides, SVGs and the vendored parser are build inputs. Module folders tie the lesson to its examples and exercises; `course/` holds shared materials and build code; `figures/` holds instructional inputs; `docs/` holds support material. The existing layout makes that distinction clear. [ENCORE paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11405857/) · [Supplementary methods](https://pure.uva.nl/ws/files/214795944/41467_2024_52446_MOESM1_ESM.pdf) · [Course resources](../course/README.md#L13)

On Windows with Python 3.14.7, a relocated Git archive ran the standard-library build from outside its checkout. The reviewer used a synthetic version, a Markdown marker and a small SVG. Two same-day runs exited successfully and produced identical bytes, with 7 modules, 38 module documents, 9 resources and 145 Dictionary terms. The reviewer asserted that the marker and SVG bytes were embedded. Removing the SVG still produced HTML and exit 0, leaving the broken relative reference. The checked-in HTML was inspected separately; byte-for-byte reproduction of the untouched committed bundle was outside that fixture. [Build paths](../course/build_dashboard.py#L27) · [Figure embedding](../course/build_dashboard.py#L294) · [Bundle output](../course/build_dashboard.py#L496)

| Criterion | Score | Evidence |
| --- | ---: | --- |
| E01 Orientation | 2/2 | Participant quick start and maintainer command are easy to find. [README](../README.md#start-the-course) · [Build guide](../CONTRIBUTING.md#under-the-hood) |
| E02 Organization | 2/2 | Module folders, generated dashboard, shared resources and figures have recognizable roles. [Course resources](../course/README.md#L13) |
| E03 Documentation | 2/2 | Module anatomy, rebuild steps and chapter conventions are documented. [Course guide](../course/README.md#L41) · [Chapter recipe](../course/chapter_recipe.md) |
| E04 Input provenance | 1/2 | Git captures primary inputs and the parser. The optional Ollama example relies on a model tag and an unpinned Python client. [Module 1 exercise](../module_01_foundations_and_privacy/README.md#exercise-run-a-model-locally) |
| E05 Traceability of steps | 2/2 | Self-check and glossary parsing, asset inlining and final packaging are identifiable. [Build pipeline](../course/build_dashboard.py#L220) |
| E06 Environment | 1/2 | Core build uses the standard library. Tested runtime/browser ranges are unstated and the slide example uses Marp `@latest`. [Slide export](../course/README.md#L103) |
| E07 Workflow verification | 1/2 | Normal and negative cases ran. Missing assets can pass, and the Windows wrapper prints Done after Python even if it fails. [Missing figure handling](../course/build_dashboard.py#L294) · [Windows wrapper](../course/update_dashboard.bat#L4) |
| E08 Output provenance | 1/2 | Bundle records release version and date. Exact input identity is absent and the current date changes the bytes across days. Hosted source links target `main`. [Build metadata](../course/build_dashboard.py#L505) · [Hosted source links](../course/dashboard_template.html#L1064) |
| E09 Portability | 2/2 | Relocated build succeeded from outside the archive. The core reader uses a single HTML file, while local source links need the extracted files. [Root resolution](../course/build_dashboard.py#L27) · [Source links](../course/dashboard_template.html#L1113) |
| E10 Handoff | 1/2 | Status files help; documentation describes a branch-protection hook as enforced while the roadmap lists it as pending and the reviewed tree lacks a tracked copy. [Decisions](../DECISIONS.md#L14) · [Roadmap](../ROADMAP.md#L13) |
| E11 Versioning | 1/2 | Release conventions and tag exist. Multiple development builds share `1.0.0`, and the separate wiki has its own revision history. [Release steps](../CONTRIBUTING.md#releasing) |
| E12 Access and reuse | 1/2 | Public checkout and ZIP provide access. The tracked course root has no explicit license or citation file. The vendored parser notice applies to the parser. [Participant download](../README.md#start-the-course) |

## Prioritized actions

Effort is an estimate for one maintainer after agreeing on the behavior.

| Order | Action | Effort and dependency | Acceptance check |
| --- | --- | --- | --- |
| 1 | Preserve progress, notes and report drafts (SOLID, Apple). Use one version-aware state decoder for startup and imports. Validate before replacing saved state, and keep an editable draft when a write fails. | Medium. Define supported previous exports and browser storage shapes first. | A normal Markdown tick survives reload; prior valid backups still load; incomplete imports leave existing work intact; quota failure leaves the draft available with copy or retry; a retry produces one saved entry. |
| 2 | Add an offline build gate (ENCORE, SOLID). Fail on missing required local assets and propagate failure through the Windows launcher. Add a small positive and negative build fixture. | Small to medium. Define which assets are required inside the bundle. | A missing required SVG yields a nonzero exit and cannot replace a known-good artifact; a valid build opens without network access. |
| 3 | Make navigation and figures work by keyboard (Apple). Move focus after route changes, support Escape and focus return for menus and lightboxes, and give figures an operable launcher. | Medium. Can proceed alongside the build gate. | Complete Orientation, navigate to Attention, open and close its figure, and return to the launcher using only the keyboard. Check a screen reader and phone viewport. |
| 4 | Improve a few shared interaction details (Apple, SOLID). Use a semantic destructive-action color, apply reduced motion to scripted scrolling, and report download outcomes accurately. | Small to medium. Reuse shared styling and download entry points. | Verify normal-size destructive text reaches 4.5:1 across module themes, scripted navigation respects reduced motion, and failed downloads offer recovery. |
| 5 | Record the build's exact inputs (ENCORE). Add an input digest or source revision and a date policy, and define how to detect stale checked-in output. Make hosted source links refer to the correct version. | Medium. Depends on the build gate and a decision about local dirty builds. | Two equivalent clean builds match under the documented rule; a source change changes the identity and flags stale output. |
| 6 | Stabilize checklist and section identity (SOLID). Migrate old saved positions to stable checklist identifiers and use one heading interpretation for extraction and linking. | Medium. Depends on the state decoder and baseline fixtures. | Reordering, editing and adding items preserves existing ticks against the correct items, fenced sample headings stay out of the outline, and existing links remain usable or migrate. |
| 7 | Make the handoff more explicit (ENCORE). Record the tested Python and browser versions and identify tested optional tool versions. Reconcile the hook documentation and ask the owner to settle course licensing and citation. | Small to medium. The reuse decision is the owner's. | A peer follows a clean build and optional exercise setup from the docs. Branch-protection guidance agrees with what is actually enforced. Reuse terms are discoverable once approved. |

Preserve the browser-only, single-file learner experience. Apple usability evidence favors that low-friction entry point, and ENCORE execution shows that the standard-library workflow is already easy to move. SOLID gives a reason to extract small state, parsing and storage boundaries inside the source. Those boundaries can compile into the same offline artifact. None of the three reviews calls for a user-facing framework migration or wholesale directory reorganization.


## Apple design follow-up

The focused follow-up scored **31/32 (96.9%)**, with **16/16 rubric checks scored**, after the earlier quick-fix result of 24/30. This is a sampled internal rubric result. The SOLID and ENCORE scores were outside this follow-up.

| Area | Updated score | Verification |
| --- | ---: | --- |
| Purpose and hierarchy | 4/4 | Orientation remains the first action and the course modules remain discoverable. |
| Layout and density | 4/4 | At a 320 CSS-pixel viewport with the largest course text setting, Dashboard, Orientation, a Foundations section, Wrap-up, Dictionary, and Preferences showed their headings and controls with no page-level horizontal overflow. |
| Familiarity and input | 4/4 | Earlier checks verified mobile menu Escape and focus on Orientation. Dictionary selection and its back action now move focus to useful destinations. |
| Accessibility | 4/4 | Real Enter and Escape events in Edge opened and closed the Attention figure dialog. Focus entered the close button and returned to the launcher; a skip link provides a direct path past navigation. |
| Typography and materials | 4/4 | Figure controls and alerts use semantic text colors. The sampled Clear all button measured 7.26:1 in light mode and 9.53:1 in dark mode. |
| Feedback and recovery | 3/4 | A simulated failed note save retained the draft and retry wrote it once. An invalid progress backup and a simulated failed write left previous progress intact; a valid backup loaded and returned focus to Load progress. General preference autosaves and download status still have uneven failure feedback. |
| Motion | 4/4 | The earlier check verified the shared scroll behavior with reduced motion enabled. |
| Charts and analytical views | 4/4 | Figure launchers work by keyboard, and Dictionary figures can expose the description from their source SVG. The Attention alternative identifies the relative strength of the three arcs. |

The dashboard was rebuilt and tested in isolated Edge profiles using synthetic notes and backup files. The 320-pixel test used the course’s text size setting. Native browser zoom, Safari, VoiceOver, live speech output and an exhaustive contrast audit remain outside this sample.


### Feedback and recovery follow-up

The sampled Apple usability score is **32/32 (100%)**, with **16/16 checks scored**. Feedback and recovery moved from 3/4 to 4/4. The other rubric checks and scope limits above still apply.

An actual Edge progress download produced valid JSON and displayed a request message that directed the reader to browser downloads. A simulated browser failure gave a retry message. A simulated viewer showed separate success and failure feedback. With browser storage blocked, text size and theme still applied to the current session, a persistent retry control stayed visible after a failed retry, and the next retry persisted both settings after storage recovered. The native viewer and assistive technology were outside this follow-up.


## ENCORE build provenance follow-up

Observed alignment is **19/24 (79.2%)** with **12/12 checks scored**. E07 previously gained one point after the missing-figure checks were verified. E08 now gains one point because the dashboard exposes a SHA-256 for its effective inputs and the builder compares the generated and tracked bytes. See the [build instructions](../CONTRIBUTING.md#under-the-hood).

A relocated checkout reproduced identical bytes with mixed LF and CRLF source inputs. Changing a synthetic course paragraph changed the fingerprint; check mode rejected stale or missing HTML without writing it. The fingerprint also appeared in the offline dashboard in Edge. Git still provides the checkout identity. The fingerprint does not pin hosted source links to a commit. The wider runtime, optional tool, and handoff findings remain open.


### Environment, handoff and source identity

The ENCORE follow-up scores **23/24 (95.8%)** with **12/12 checks scored**. E04 now records the full Ollama manifest digest and client version for a tested synthetic prompt. E06 records the tested core build and browser, and pins Marp. E10 corrects the branch-hook decision to match the roadmap. E11 maps the published bundle's fingerprint to a Git commit, and the hosted source link uses that commit. [Tested environment](reproducibility.md) · [Source pin workflow](../CONTRIBUTING.md#under-the-hood) · [Branch decision](../DECISIONS.md)

The optional checks produced a short local greeting using Ollama and valid PDF and PPTX exports of the Module 1 slides using the official, checksum-verified Marp CLI. The hosted source link was verified in Edge. A relocated copy reproduced the pinned HTML, and an edited source file made the check fail and the next build drop the old pin.

E12 remains 1/2. The README requests attribution to the course and its author. The owner chose informal attribution guidance, with no formal course license added. [Course attribution](../README.md#learn-more)
