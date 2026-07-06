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
| --clips-per-beat | -c | The amount of clips to be displayed per audio beat. Can be a decimal number but must be greater than 0. Default: 1 | POSITIVE_NUMBER_NOT_0 |
| --darken | -d | The intensity of the darkening effect to be applied to every clip or 'off' to deactivate darkening. 0 means normal, 1 means all black. Default: off | POSITIVE_NUMBER or 'off' |
| --vignette | -V | The base brightness of the vignette effect to be applied to every clip or 'off' to deactivate. Default: 0.8 | POSITIVE_NUMBER or 'off' |
| <a id="transition-arg"></a> --transitions | -t | A list allowed transitions between graphic clips. Can be either a comma-separated list of names with optional weight or a transition abbreviation. Refer to the [transition CLI documentation](#cli-examples) for further information | NAME,NAME,NAME... or INTEGER |
| --seed |  | The seed to be used for random choices. When generating multiple videos with the same seed, the choices are guaranteed to be the same random sequence as long as no other parameters interfer with the sample space. Can be any text | TEXT |

---

## Transitions

The script supports various randomly chosen transitions to be rendered between graphic clips. The sample space can be limited using the [optional `--transitions` argument](#transition-arg). The transition argument takes either a comma-separated list of transition names with an optional weight or a transition abbreviation.

The following transitions are supported:

| Name | Description | Abbreviation Position |
| ---- | ----------- | --------------------- |
| jump | A classic cut between two clips, jumping from one to the other once it is finished. | $`1st`$ |
| black-fade | The previous clip becomes darker over time until it is completely black. The next clip starts of completely dark and lights up to normal brightness. | $`2nd`$ |
| cross-fade | The previous clip becomes more transparent over time until it vanishes completely. Simultaneously, the other clip becomes visible below the first one and get progressively less transparent, replacing the first clip. | $`3rd`$ |
| zoom-out | The previous clip becomes smaller over time until it reaches half its original size. The next clip starts of at half the size and becomes bigger until it reaches normal dimensions, creating the illusion of a camera zooming out and in. | $`4th`$ |
| zoom-out-fade | The previous clip becomes smaller over time until it reaches half its original size. At the same time it darkens until it's completely black. The next clip starts of at half the size and becomes bigger until it reaches normal dimensions while also fading in from a previously completely black clip. | $`5th`$ |
| zoom-in | The previous clip becomes bigger over time until it reaches 150% of its original size. The next clip starts of at 150% size and becomes smaller until it reaches normal dimensions, creating the illusion of a camera zooming in and out | $`6th`$ |
| zoom-in-fade | The previous clip becomes bigger over time until it reaches 150% of its original size. At the same time it darkens until it's completely black. The next clip starts of at 150% size and becomes bigger until it reaches normal dimensions while also fading in from a previously completely black clip. | $`7th`$ |
| slide-out | The previous clip slides to the side, revealing the next clip lying under it. The direction to slide out _(up, down, left, right)_ is randomly chosen | $`8th`$ |
| slide-in | The next clip slides in from the side, covering the previous clip below it. The direction to slide in from _(up, down, left, right)_ is randomly chosen | $`9th`$ |
| walk | The current clip slides out in one direction while the next one is sliding in from the opposite one, creating the illusion of both clips existing next to one another with the camera moving from focusing the first to the second.  The direction to walk in _(up, down, left, right)_ is randomly chosen | $`10th`$ |

---

### CLI Examples

#### Normal Form

Let's assume we wanted to express the combination of the transitions `black-fade` and `cross-fade` which can be found in the table above. To do so, we simply combine both names to a comma-separated list:
```
black-fade,cross-fade
```

If we now want the randomizer to prefer the black-fade transition over cross-fade, we can add a weight. This weight is a single-digit number ($`0-9`$) that is prepended to the name using a `:`. If no weight is given, a value of $`1`$ is assumed.
```
2:black-fade,cross-fade
```
This means, if the randomizer makes 3 choices, on average the black-fade is chosen twice and the cross-fade just one.

To compact the list, we can also omit the `:`
```
2black-fade,cross-fade
```

#### Abbreviated

Instead of writing down the entire list, we can also abbreviate the normal form by just writing down the weights for each transition. Those weight digits are concatenated to a single line where the transition the digit belongs to is denoted by the digit's position from left to right. The mapping can be found in the [transition table](#transitions). To the right of the abbreviation, every leftover position is implicitely set to $`0`$

This example

$$ 1111 $$

means that the first four transitions _(`jump`,`black-fade`,`cross-fade`,`zoom-out`)_ should be active with a weight of $`1`$. Because the entire right of the abbreviation is implicitely $`0`$, the expanded version looks like $`1111(0000000...)`$ - All other transitions have weight of $`0`$ and are therefore turned off.

Likewise,

$$ 0200104 $$

represents a combination where `black-fade` has a weigth of $`2`$, `zoom-out-fade` has a weight of $`1`$ and `zoom-in-fade` a weight of $`4`$. All other transitions are not active.
