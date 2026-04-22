import sys
import subprocess
import os

def main():
    print("Starting DDR AI Builder Streamlit App...\n")
    # Launch Streamlit
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
    except KeyboardInterrupt:
        print("\nApp stopped by user.")
    except Exception as e:
        print(f"Error launching Streamlit: {e}")

if __name__ == "__main__":
    main()