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

## Optional Arguments
