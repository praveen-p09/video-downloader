from pytube import YouTube
import sys

# Define progress callback function to update the same line dynamically
def progress_func(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progress_message = f"Downloaded {bytes_downloaded} of {total_size} bytes ({percentage:.2f}%)"
    sys.stdout.write('\r' + progress_message)
    sys.stdout.flush()

def complete_func(stream, file_path):
    print(f"\nDownload complete! File saved to: {file_path}")

try:
    # Asking user to input the YouTube URL
    url = input("Enter the YouTube URL: ")
    
    yt = YouTube(url,
        on_progress_callback=progress_func,
        on_complete_callback=complete_func
    )
    
    # Get the English caption (subtitles) if available
    caption = yt.captions.get_by_language_code('en')
    
    # Print video details
    print("Title:", yt.title)
    print("Views:", yt.views)
    
    # Generate and print subtitles if available
    if caption:
        print(caption.generate_srt_captions())
    else:
        print("No English captions available.")
    
    # Get the highest resolution stream
    yd = yt.streams.get_highest_resolution()
    
    # Download the video to the current directory
    yd.download()
    
except Exception as e:
    print("An error occurred:", str(e))
