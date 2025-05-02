import os
import shutil

def clear_sessions():
    session_dir = 'flask_session'
    
    # Check if directory exists
    if os.path.exists(session_dir):
        print(f"Clearing sessions from {session_dir}...")
        try:
            # Remove all files in the directory
            for filename in os.listdir(session_dir):
                file_path = os.path.join(session_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted: {file_path}")
            print("All session files cleared successfully!")
        except Exception as e:
            print(f"Error clearing sessions: {e}")
    else:
        print(f"Session directory {session_dir} does not exist.")
        # Create the directory
        try:
            os.makedirs(session_dir)
            print(f"Created empty session directory: {session_dir}")
        except Exception as e:
            print(f"Error creating session directory: {e}")

if __name__ == "__main__":
    clear_sessions()
    print("You can now start the Flask application with: python main.py") 