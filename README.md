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

## How it Works

The base script operates in 5 main steps:

1. **Analyze audio beats**

    By analyzing the provided audio file, the script figures out the timestamps of the audio's beats

2. **Generate beat-syncronized graphic clips**

    The graphics are selected and prepared for editing. This includes adjusting the graphics to a length that matches the audio's beats and applying filters like vignette

3. **Apply clip transitions**

    Adjacent clips are concatenated using a randomly selected transition from the [pool of available transitions](#transition-arg)

4. **Export audio**

    The audio is exported for later use with the final edit

5. **Render video**
    
    The video is rendered based on the generated clips, the audio is added and the result is stored

Depending on the exact configuration, additional steps might be added to the process.

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

---

## Transitions

The script supports various randomly chosen transitions to be rendered between graphic clips. The sample space can be limited using the [optional `--transitions` argument](#transition-arg).

The transition argument takes either a comma-separated list of transition names or a bitmask. A bitmask is a way to represent a combination as a compact number. Essentially, it is computed by adding up all the bitmask values of the chosen elements.

The following transitions are supported:

| Name | Description | Bitmask Value |
| ---- | ----------- | ------------- |
| jump | A classic cut between two clips, jumping from one to the other once it is finished. | $`2^0 = 1`$ |
| black-fade | The previous clip becomes darker over time until it is completely black. The next clip starts of completely dark and lights up to normal brightness. | $`2^1 = 2`$ |
| cross-fade | The previous clip becomes more transparent over time until it vanishes completely. Simultaneously, the other clip becomes visible below the first one and get progressively less transparent, replacing the first clip. | $`2^2 = 4`$ |
| zoom-out | The previous clip becomes smaller over time until it reaches half its original size. The next clip starts of at half the size and becomes bigger until it reaches normal dimensions, creating the illusion of a camera zooming out and in. | $`2^3 = 8`$ |
| zoom-out-fade | The previous clip becomes smaller over time until it reaches half its original size. At the same time it darkens until it's completely black. The next clip starts of at half the size and becomes bigger until it reaches normal dimensions while also fading in from a previously completely black clip. | $`2^4 = 16`$ |
| zoom-in | The previous clip becomes bigger over time until it reaches 150% of its original size. The next clip starts of at 150% size and becomes smaller until it reaches normal dimensions, creating the illusion of a camera zooming in and out | $`2^5 = 32`$ |
| zoom-in-fade | The previous clip becomes bigger over time until it reaches 150% of its original size. At the same time it darkens until it's completely black. The next clip starts of at 150% size and becomes bigger until it reaches normal dimensions while also fading in from a previously completely black clip. | $`2^6 = 64`$ |
| slide-out | The previous clip slides to the side, revealing the next clip lying under it. The direction to slide out _(up, down, left, right)_ is randomly chosen | $`2^7 = 128`$ |
| slide-in | The next clip slides in from the side, covering the previous clip below it. The direction to slide in from _(up, down, left, right)_ is randomly chosen | $`2^8 = 256`$ |
| walk | The current clip slides out in one direction while the next one is sliding in from the opposite one, creating the illusion of both clips existing next to one another with the camera moving from focusing the first to the second.  The direction to walk in _(up, down, left, right)_ is randomly chosen | $`2^9 = 512`$ |

---

### Bitmask example

Let's assume we wanted to express the combination `black-fade,cross-fade` in its shorter bitmask form. To do so, we look at the bitmask values of these transitions _($`2`$ and $`4`$)_ and add them up:
$$ 2 + 4 = 6 $$
To **edit-maker**, "$`6`$" and `black-fade,cross-fade` mean the same thing.

Similarily, this means that selecting all transitions but `jump` can be expressed as `black-fade,cross-fade,zoom-out,zoom-out-fade,zoom-in,zoom-in-fade,slide-out,slide-in,walk` and "$`1022`$" since
$$ 2 + 4 + 8 + 16 + 32 + 64 + 128 + 256 + 512 = 1022 $$
