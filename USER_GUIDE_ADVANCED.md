# Advanced User Guide

## Professional Video Features

### 1. Color Grading

Apply professional color grades to your videos:

```python
from backend.color_grading import ColorGrading

grader = ColorGrading()

# Apply cinematic grade
grader.apply_color_grade(frame, preset='cinematic')

# Available presets:
# - cinematic: Hollywood-style grading
# - warm: Warm, inviting tones
# - cool: Cool, blue tones
# - vintage: Retro, faded look
# - dramatic: High contrast, moody
```

### 2. Video Effects

Add professional effects:

```python
from backend.video_effects import VideoEffects

effects = VideoEffects()

# Apply blur
effects.apply_effect(video_path, 'blur', output_path, strength=15)

# Apply sepia tone
effects.apply_effect(video_path, 'sepia', output_path)

# Adjust brightness
effects.apply_effect(video_path, 'brightness', output_path, value=30)
```

### 3. Subtitle Generation

Add subtitles automatically:

```python
from backend.subtitle_generator import SubtitleGenerator

generator = SubtitleGenerator()

# Auto-generate from prompt
subtitle_path = generator.create_auto_subtitles(
    video_path,
    prompt="Your video description",
    output_filename="subtitles.srt"
)

# Add to video
generator.add_subtitles_to_video(video_path, subtitle_path)
```

### 4. Watermark Overlay

Add watermarks and logos:

```python
from backend.watermark_overlay import WatermarkOverlay

overlay = WatermarkOverlay()

# Add text watermark
overlay.add_text_watermark(
    frame,
    text="© Your Brand",
    position='bottom-right',
    opacity=0.5
)

# Add logo
overlay.add_logo_watermark(
    frame,
    logo_path='logo.png',
    position='top-left',
    scale=0.1
)
```

### 5. Frame Interpolation

Create smooth slow motion:

```python
from backend.frame_interpolation import FrameInterpolation

interpolator = FrameInterpolation()

# Create slow motion (2x slower)
interpolator.create_slow_motion(
    video_path,
    output_path,
    slow_factor=2.0,
    method='optical_flow'
)

# Increase FPS
interpolator.increase_fps(video_path, output_path, target_fps=60)
```

### 6. Video Stabilization

Stabilize shaky footage:

```python
from backend.video_stabilization import VideoStabilization

stabilizer = VideoStabilization()

# Stabilize video
stabilizer.stabilize_video(
    input_path,
    output_path,
    smoothing_radius=30
)
```

### 7. Audio Effects

Enhance audio:

```python
from backend.audio_effects import AudioEffects

audio_fx = AudioEffects()

# Apply fade in/out
audio_fx.apply_fade_in(audio_data, sample_rate, duration=1.0)
audio_fx.apply_fade_out(audio_data, sample_rate, duration=1.0)

# Add echo
audio_fx.add_echo(audio_data, sample_rate, delay=0.3, decay=0.5)

# Add reverb
audio_fx.add_reverb(audio_data, sample_rate, room_size=0.5)
```

### 8. Transition Effects

Add smooth transitions:

```python
from backend.transition_effects import TransitionEffects

transitions = TransitionEffects()

# Apply crossfade
transitions.apply_crossfade(clip1, clip2)

# Apply zoom
transitions.apply_zoom(clip, zoom_in=True)

# Create sequence with transitions
transitions.create_transition_sequence(clips, transition_type='crossfade')
```

### 9. Template System

Use predefined templates:

```python
from backend.template_manager import TemplateManager

manager = TemplateManager()

# List templates
templates = manager.list_templates()

# Apply template
settings = manager.apply_template('youtube', prompt)
```

### 10. Batch Processing

Process multiple videos:

```python
from backend.batch_processor import BatchProcessor

processor = BatchProcessor(max_workers=2)

# Add jobs
job_ids = processor.add_multiple_jobs([
    "ocean waves",
    "mountain sunset",
    "city lights"
])

# Start processing
processor.start(generate_video)

# Monitor progress
stats = processor.get_queue_stats()
```

## Advanced Workflows

### Workflow 1: Professional Video Production

```python
# 1. Generate base video
result = generate_video("ocean sunset")

# 2. Apply color grading
graded = apply_color_grade(result['video_path'], 'cinematic')

# 3. Add stabilization
stabilized = stabilize_video(graded)

# 4. Add watermark
watermarked = add_watermark(stabilized, "© Your Brand")

# 5. Add subtitles
final = add_subtitles(watermarked, prompt)
```

### Workflow 2: Social Media Content

```python
# 1. Use template
settings = apply_template('tiktok', prompt)

# 2. Generate video
result = generate_video(prompt, settings)

# 3. Add effects
effected = apply_effect(result['video_path'], 'vignette')

# 4. Add music
final = add_background_music(effected, 'energetic')
```

### Workflow 3: Slow Motion Creation

```python
# 1. Generate video
result = generate_video("fast action scene")

# 2. Create slow motion
slow_mo = create_slow_motion(result['video_path'], slow_factor=3.0)

# 3. Add dramatic color grade
graded = apply_color_grade(slow_mo, 'dramatic')

# 4. Export
export_video(graded, profile='high')
```

## Tips & Best Practices

### Color Grading
- Use 'cinematic' for professional look
- 'warm' for happy, inviting content
- 'cool' for tech, modern content
- 'dramatic' for intense scenes

### Effects
- Less is more - don't over-process
- Apply effects in order: stabilize → grade → effects
- Test on short clips first

### Subtitles
- Keep text short (5-7 words per segment)
- Use high contrast colors
- Position at bottom for readability

### Watermarks
- Use 50-70% opacity
- Position in corner
- Keep size small (10-15% of frame)

### Performance
- Process in batches for multiple videos
- Use lower quality for previews
- Cache intermediate results

## Troubleshooting

### Issue: Effects too strong
**Solution**: Reduce effect parameters (opacity, strength, etc.)

### Issue: Slow processing
**Solution**: Use lower resolution or reduce effect complexity

### Issue: Audio sync issues
**Solution**: Ensure consistent frame rate throughout pipeline

### Issue: Quality loss
**Solution**: Use lossless intermediate formats, compress only at end

## Next Steps

1. Experiment with different presets
2. Combine multiple effects
3. Create custom workflows
4. Automate with batch processing
5. Integrate with your applications

For more help, see:
- API_INTEGRATION_GUIDE.md
- PERFORMANCE_TUNING.md
- TROUBLESHOOTING.md
