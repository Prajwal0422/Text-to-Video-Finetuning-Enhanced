# NEXUS VISION - Testing Suite

## Overview

This testing suite provides **deterministic, verifiable validation** of the entire video generation pipeline. No assumptions. No optimistic status. Runtime proof only.

## Test Files

### Phase 1: Environment Verification
**File:** `verify_environment.py`

Verifies:
- Python version (3.8+)
- MoviePy installation
- imageio installation
- FFmpeg availability
- FFmpeg execution

**Run:**
```bash
python verify_environment.py
```

**Expected:** All checks pass, FFmpeg version printed

---

### Phase 2: Raw Clip Validation
**File:** `test_download_and_normalize.py`

Tests:
- Download clip from Pexels
- Streaming download (no corruption)
- File size validation (> 100KB)
- FFmpeg normalization
- Normalized file validation

**Run:**
```bash
python test_download_and_normalize.py
```

**Expected:** 
- Raw clip downloaded
- Normalized clip created
- Both files > minimum size

**Output:**
- `outputs/test_clips/raw_test_clip.mp4`
- `outputs/test_clips/normalized_test_clip.mp4`

---

### Phase 3: Single Clip Export
**File:** `test_single_clip_export.py`

Tests:
- Load normalized clip with MoviePy
- Duration validation (> 0)
- Safe trimming with min()
- Video export
- Output verification

**Run:**
```bash
python test_single_clip_export.py
```

**Expected:**
- Clip loads successfully
- Duration > 0
- Export completes
- Output file playable

**Output:**
- `outputs/test_clips/single_test_output.mp4`

**Verify:**
```bash
vlc outputs/test_clips/single_test_output.mp4
```

---

### Phase 4: Multi-Clip Merge
**File:** `test_multi_clip_merge.py`

Tests:
- Load multiple clips
- Validate each clip duration
- Concatenate with method="compose"
- Export merged video
- Duration verification

**Run:**
```bash
python test_multi_clip_merge.py
```

**Expected:**
- 3 clips loaded
- All durations valid
- Concatenation successful
- Output duration = sum of inputs

**Output:**
- `outputs/test_clips/multi_test_output.mp4`

**Verify:**
```bash
vlc outputs/test_clips/multi_test_output.mp4
```

---

### Phase 5: Video Editor Rebuild
**File:** `video_editor_rebuilt.py`

Rebuilt video editor with:
- Clear debug prints at each step
- Explicit validation
- Fail-loud error handling
- No silent returns
- No nested error suppression

**Features:**
- `normalize_video()` - FFmpeg pre-processing
- `load_and_validate_clip()` - Strict validation
- `trim_clip()` - Safe trimming
- `process_clip()` - Full pipeline
- `create_video()` - Main entry point

**Run:**
```bash
python video_editor_rebuilt.py
```

**Expected:** Initialization successful, settings printed

---

### Phase 6: Final Integration Test
**File:** `final_pipeline_test.py`

Tests:
- Full end-to-end pipeline
- Timing breakdown
- Final verification checklist
- Playback instructions

**Run:**
```bash
python final_pipeline_test.py
```

**Expected:**
- Video created successfully
- Duration > 5s (or valid for input)
- File size > 200KB
- All checks pass

**Output:**
- `outputs/videos/final_pipeline_test_output.mp4`

**Verify:**
```bash
vlc outputs/videos/final_pipeline_test_output.mp4
```

---

## Master Test Runner

**File:** `run_all_tests.py`

Runs all 6 phases sequentially. Stops on first failure.

**Run:**
```bash
python run_all_tests.py
```

**Expected:**
- All phases pass
- Total time < 5 minutes
- 3 output videos created

---

## Success Criteria

The system is considered **STABLE** only when:

1. ✅ All 6 phases pass
2. ✅ `single_test_output.mp4` plays in VLC
3. ✅ `multi_test_output.mp4` plays in VLC
4. ✅ `final_pipeline_test_output.mp4` plays in VLC
5. ✅ All videos play in browser
6. ✅ All videos have duration > 0
7. ✅ All videos have file size > minimum

---

## Quick Start

### Option 1: Run All Tests
```bash
cd backend
python run_all_tests.py
```

### Option 2: Run Individual Phases
```bash
cd backend
python verify_environment.py
python test_download_and_normalize.py
python test_single_clip_export.py
python test_multi_clip_merge.py
python final_pipeline_test.py
```

---

## Troubleshooting

### Phase 1 Fails
- Install dependencies: `pip install -r requirements.txt`
- Verify Python 3.8+: `python --version`

### Phase 2 Fails
- Check internet connection
- Set Pexels API key: `export PEXELS_API_KEY="your_key"`
- Check FFmpeg: `ffmpeg -version`

### Phase 3 Fails
- Run Phase 2 first
- Check MoviePy installation
- Verify normalized clip exists

### Phase 4 Fails
- Run Phase 2 first
- Check disk space
- Verify FFmpeg working

### Phase 6 Fails
- Run Phases 2-4 first
- Check all test clips exist
- Verify video_editor_rebuilt.py loads

---

## Output Files

After successful run:

```
outputs/
├── test_clips/
│   ├── raw_test_clip.mp4              (Phase 2)
│   ├── normalized_test_clip.mp4       (Phase 2)
│   ├── test_clip_1.mp4                (Phase 4)
│   ├── test_clip_2.mp4                (Phase 4)
│   ├── test_clip_3.mp4                (Phase 4)
│   ├── single_test_output.mp4         (Phase 3) ⭐
│   └── multi_test_output.mp4          (Phase 4) ⭐
├── normalized/
│   └── norm_*.mp4                     (Cached normalized clips)
└── videos/
    └── final_pipeline_test_output.mp4 (Phase 6) ⭐
```

⭐ = Files to verify playback

---

## Verification Commands

### VLC
```bash
vlc outputs/test_clips/single_test_output.mp4
vlc outputs/test_clips/multi_test_output.mp4
vlc outputs/videos/final_pipeline_test_output.mp4
```

### Browser
Open in browser:
- `file:///path/to/outputs/test_clips/single_test_output.mp4`
- `file:///path/to/outputs/test_clips/multi_test_output.mp4`
- `file:///path/to/outputs/videos/final_pipeline_test_output.mp4`

### FFprobe (Check Duration)
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 outputs/test_clips/single_test_output.mp4
```

---

## Critical Rules

1. **No Assumptions** - Every step verified
2. **Fail Loudly** - Exceptions raised, not suppressed
3. **Runtime Proof** - Print actual values, not expected
4. **Abort on Failure** - Don't continue if step fails
5. **Verify Output** - Reload and check duration

---

## Next Steps After Success

Once all tests pass:

1. **Integrate with main system**
   - Replace `backend/video_editor.py` with `video_editor_rebuilt.py`
   - Update imports in `video_generator.py`

2. **Test with real prompts**
   - Run full pipeline with user prompts
   - Verify WebSocket integration
   - Test UI generation

3. **Production deployment**
   - Run tests on production server
   - Verify all dependencies installed
   - Test with production API keys

---

## Support

If tests fail:
1. Read error messages carefully
2. Check which phase failed
3. Run that phase individually
4. Check prerequisites for that phase
5. Verify file outputs exist

---

**Built for deterministic, verifiable video generation**
