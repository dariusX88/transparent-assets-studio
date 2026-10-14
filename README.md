# Transparent Assets Studio

Make product images in ChatGPT with a real transparent background, then put them on any background and in any format in one offline HTML studio.

Two parts:

1. **A skill for ChatGPT** (`SKILL.md`). It tells ChatGPT how to create and edit your product images as transparent PNGs, keep a collection consistent, and build your own studio file.
2. **The studio** (`studio.html`). Double click it. It opens in your browser, works offline and uploads nothing. Show one, two or all products, switch backgrounds and formats (banner, slide, square post), check the transparency, export, and save a project you can reopen.

## Get started

1. Download the zip from [Releases](../../releases/latest) and unzip it.
2. Open `studio.html` to see the included example.
3. In ChatGPT open **Skills**, click **Add**, then **Upload from your computer**, and upload this folder as a zip. (Codex: copy the folder into `~/.agents/skills/`.)
4. Ask: *"Use Transparent Assets Studio. My brand is ... Create the first product as a transparent PNG."* Then ask it to build your own studio with your products.

Full guide: [START-HERE.md](START-HERE.md).

## Good to know

- The studio itself does not generate images. ChatGPT does, on the plan you already pay for. No API key.
- Look at every image before you use it. In my test, ChatGPT once said an image was complete when it was cut off at the bottom.
- Nothing saves on its own. Use **Save project with all images**.

Based on the transparent assets example in the OpenAI Cookbook. Packaged with Codex. Shared by [Darius X AI](https://www.youtube.com/@DariusXai).
