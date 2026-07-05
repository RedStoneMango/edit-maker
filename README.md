# Edit Maker

Easily generate TikTok edits purely by providing an audio and image files. No video editing skills needed.

## Usage

The base script can be called using

```sh
$ edit-maker AUDIO OUTPUT GRAPHICS [GRAPHICS...]
```

Where:

| AUDIO | OUTPUT | GRAPHICS |
| ----- | ------ | -------- |
| One audio file to use as music for the edit | One video file to save the edit as | An arbitrary amount of files containing the visual content to be shown in the edit. Can be imagess, videos, animated GIFs or a mixture of the above |

For additional options, see the [optional arguments](#optional-arguments) section.

**Example**:
```sh
$ edit-maker audio.mp3 my-edit.mp4 image1.jpg image2.png animated.gif video.mp4
```

The above creates an edit as *my-edit.mp4* using the music *audio.mp3* and featuring the contents *image1.jpg*, *image2.png*, *animated.gif* and *video.mp4*.

---

## Optional Arguments

The script accepts a set of optional arguments to customize your edits even further:

| Name | Abbreviation | Decription | Value Format |
| ---- | ------------ | ---------- | ------------ |
| --help | -h | Show a help message in the terminal and exit |  |
| --beat-tightness |  | A (decimal) number specifying the tightness of the detected audio beat distribution around the tempo of the audio file. Must be greater or equal to 0. The detected beats are used to align the hraphic clips with the audio | POSITIVE_NUMBER |
| --size | -s | The size of the edit in pixels. This will scale all graphics to this value while respecting the aspect ratio. Without this option, the size is the max width/height of the provided graphics. To specify the fill of leftover areas, have a look at `--background-blur` | WIDTH,HEIGHT or WIDTHxHEIGHT or WIDTH×HEIGHT |
| --background-blur | -B | Enables background blur for graphics whose size does not match the canvas size. Instead of the standard black area, the outer part of the graphic will be a blurred version of the graphic itself |  |
| --graphic-beats | -b | The amount of audio beats a graphic should be displayed. Higher values mean that individual graphics are visible for a longer time. Default: 1 | POSITIVE_NUMBER_NOT_0 |
| --darken | -d | The intensity of the darkening effect to be applied to every clip or 'off' to deactivate darkening. 0 means normal, 1 means all black. Default: off | POSITIVE_NUMBER or 'off' |
| --vignette | -V | The base brightness of the vignette effect to be applied to every clip or 'off' to deactivate. Default: 0.8 | POSITIVE_NUMBER or 'off' |
| <a id="transition-arg"></a> --transitions | -t | A list allowed transitions between graphic clips. Can be either a comma-separated list of names or a bitmask. Refer to the [transition documentation](#transitions) for name and index information | NAME,NAME,NAME... or INTEGER |
| --seed |  | The seed to be used for random choices. When generating multiple videos with the same seed, the choices are guaranteed to be the same random sequence as long as no other parameters interfer with the sample space. Can be any text | TEXT |
