# Transparent Assets Studio

Open **studio.html** in a browser. Circuit is the included example; you can use this workspace for another brand or product collection. Everything needed for the demo is embedded, so the studio runs offline and does not depend on someone else's localhost address.

## Create and edit with AI

Install the skill in a compatible ChatGPT or Codex environment, then ask:

> Open Transparent Assets Studio and create a product collection for my brand using built-in image generation. Save the original transparent PNGs and a studio project I can reopen.

Or, for a revision:

> Use Transparent Assets Studio to edit this product. Change the cap to matte black, preserve the bottle shape and label, and save a new version.

Generating and editing images requires the host's image tools and the user's own available plan/usage. The browser studio composes existing images and does not generate images or make API calls itself. The skill defaults to built-in generation; it does not include an API key or automatically switch to paid APIs.

## Use the studio

- Add one or several PNGs with **Add product PNGs**.
- Select the featured product and one, two, or all products.
- Change the brand, headline, background, format, and size.
- Inspect the transparency grid; export a composition or the featured original PNG.
- Use **Save project with all images** before closing. This downloads a `.studio.json` containing the images, names, and settings.
- Use **Open saved project** to resume. Share that project file along with `studio.html` for someone else to continue.

Browser edits are temporary until saved. Project saving is explicit rather than dependent on browser storage quotas. There are no store connectors, background agents, publishing actions, credentials, or cloud synchronization.

## Install the skill

### ChatGPT

Where your ChatGPT account provides standalone skill import, open **Skills**, choose **New Skill**, then **Upload from your computer**, and upload the skill ZIP. In a new chat, select **Transparent Assets Studio** with `@` or describe the task directly. Availability and installation controls depend on your app/workspace. Local Codex installation does not automatically install it in ChatGPT.

If standalone import is unavailable, the HTML still works. You can provide `SKILL.md` to a chat as a workflow brief, but an attachment is not the same as installing a reusable skill. The optional plugin ZIP is a portable skills-only package for environments that support custom plugins or marketplace installation; it is not publicly published or universally installed.

### Codex

Copy this whole `transparent-assets-studio` folder into your personal `.agents/skills` directory. On macOS/Linux this is `~/.agents/skills/transparent-assets-studio`; on Windows use your user-profile `.agents/skills` directory. Start a new chat and invoke `$transparent-assets-studio`. Skill detection is automatic in supported clients; restart if it does not appear.

## Share it

Send **transparent-assets-studio.zip** to another person. They can unzip it and open `studio.html`, or install the bundled skill in a compatible environment. All asset paths are relative. Circuit's PNGs and original generation prompts are under `examples/circuit/`.

The package includes an offline studio, skill instructions, a reusable template, a standard-library-only project builder, and the Circuit example. Python 3.9 or later is needed only for the optional builder; opening the studio itself needs only a modern browser.

## Build another studio

Give your AI assistant a product brief and reference images. Have it generate or edit PNGs, save a manifest as described in `references/project-format.md`, and use `scripts/studio.py` to build a new standalone HTML file. The builder validates actual PNG pixels, confines file references to the project folder, and refuses to overwrite existing output files.

## Platform references

- [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins)
- [Build and install skills](https://learn.chatgpt.com/docs/build-skills)
- [ChatGPT skill upload instructions](https://developers.openai.com/cookbook/examples/chatgpt/chatgpt_prompt_guide/chatgpt_prompt_guide)
- [Portable plugin packaging](https://developers.openai.com/plugins/build/plugins)
