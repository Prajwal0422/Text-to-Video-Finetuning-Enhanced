"""
MASTER TEST RUNNER
Runs all phases sequentially with clear status reporting
"""

import sys
import subprocess
import time

def run_phase(phase_num, phase_name, script_name):
    """Run a single test phase"""
    print("\n" + "=" * 70)
    print(f"PHASE {phase_num}: {phase_name}")
    print("=" * 70)
    print(f"Running: {script_name}")
    print("-" * 70)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=".",
            capture_output=False,
            text=True,
            timeout=300  # 5 minute timeout per phase
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print("-" * 70)
            print(f"✅ PHASE {phase_num} PASSED in {elapsed:.1f}s")
            print("=" * 70)
            return True
        else:
            print("-" * 70)
            print(f"❌ PHASE {phase_num} FAILED (exit code {result.returncode})")
            print("=" * 70)
            return False
            
    except subprocess.TimeoutExpired:
        print("-" * 70)
        print(f"❌ PHASE {phase_num} TIMEOUT (5 minutes)")
        print("=" * 70)
        return False
    except Exception as e:
        print("-" * 70)
        print(f"❌ PHASE {phase_num} ERROR: {e}")
        print("=" * 70)
        return False

def main():
    print("=" * 70)
    print("NEXUS VISION - COMPLETE PIPELINE VERIFICATION")
    print("=" * 70)
    print("This will run all 6 phases sequentially")
    print("Each phase must pass before proceeding to the next")
    print("=" * 70)
    
    input("\nPress ENTER to start...")
    
    phases = [
        (1, "ENVIRONMENT VERIFICATION", "verify_environment.py"),
        (2, "RAW CLIP VALIDATION", "test_download_and_normalize.py"),
        (3, "SINGLE CLIP EXPORT", "test_single_clip_export.py"),
        (4, "MULTI-CLIP MERGE", "test_multi_clip_merge.py"),
        (5, "VIDEO EDITOR REBUILD", "video_editor_rebuilt.py"),
        (6, "FINAL INTEGRATION", "final_pipeline_test.py"),
    ]
    
    results = []
    start_time = time.time()
    
    for phase_num, phase_name, script_name in phases:
        success = run_phase(phase_num, phase_name, script_name)
        results.append((phase_num, phase_name, success))
        
        if not success:
            print(f"\n❌ STOPPING: Phase {phase_num} failed")
            break
        
        # Brief pause between phases
        if phase_num < 6:
            time.sleep(1)
    
    total_time = time.time() - start_time
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    for phase_num, phase_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"Phase {phase_num}: {phase_name:30s} {status}")
    
    print("=" * 70)
    print(f"Total time: {total_time:.1f}s")
    print("=" * 70)
    
    # Check if all passed
    all_passed = all(success for _, _, success in results)
    
    if all_passed:
        print("\n" + "=" * 70)
        print("✅ ALL PHASES PASSED - SYSTEM VERIFIED")
        print("=" * 70)
        print("\nThe video generation pipeline is now proven to work.")
        print("Test files created:")
        print("  - outputs/test_clips/single_test_output.mp4")
        print("  - outputs/test_clips/multi_test_output.mp4")
        print("  - outputs/videos/final_pipeline_test_output.mp4")
        print("\nPlay these files in VLC or browser to confirm.")
        print("=" * 70)
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ VERIFICATION FAILED")
        print("=" * 70)
        print("\nFix the failing phase before proceeding.")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ ABORTED BY USER")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
