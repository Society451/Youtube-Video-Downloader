import os
import time
import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def download_video():
    video_url = url_entry.get()
    output_path = path_entry.get()
    custom_name = name_entry.get()
    write_subs = write_subs_var.get()
    embed_subs = embed_subs_var.get()
    quality = quality_var.get()
    merge_format = merge_format_var.get()
    video_format = video_format_var.get()

    if not video_url:
        messagebox.showerror("Error", "Please enter a video URL")
        return

    if not output_path:
        messagebox.showerror("Error", "Please select an output path")
        return

    start_time = time.time()
    log_text.insert(tk.END, 'Starting download...\n')

    try:
        ydl_opts = {'outtmpl': os.path.join(output_path, f'{custom_name}.%(ext)s') if custom_name else os.path.join(output_path, '%(title)s.%(ext)s')}
        
        if write_subs:
            ydl_opts['writesubtitles'] = True
        if embed_subs:
            ydl_opts['embedsubtitles'] = True
        if quality:
            ydl_opts['format'] = quality
        if merge_format:
            ydl_opts['merge_output_format'] = merge_format
        if video_format:
            ydl_opts['format'] = video_format

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        elapsed_time = time.time() - start_time
        log_text.insert(tk.END, 'Download completed!\n')
        log_text.insert(tk.END, f'Completed in {elapsed_time:.2f} seconds\n')
    except Exception as e:
        log_text.insert(tk.END, f'Error: {e}\n')

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# URL input
tk.Label(root, text="Video URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Output path input
tk.Label(root, text="Output Path:").grid(row=1, column=0, padx=10, pady=10)
path_entry = tk.Entry(root, width=50)
path_entry.grid(row=1, column=1, padx=10, pady=10)
path_entry.insert(0, os.path.join(os.path.expanduser('~'), 'Downloads'))

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Custom file name input
tk.Label(root, text="Save As (blank downloads it as default name):").grid(row=2, column=0, padx=10, pady=10)
name_entry = tk.Entry(root, width=50)
name_entry.grid(row=2, column=1, padx=10, pady=10)

# Write subtitles checkbox
write_subs_var = tk.BooleanVar()
write_subs_check = tk.Checkbutton(root, text="Download Subtitles", variable=write_subs_var)
write_subs_check.grid(row=3, column=0, padx=10, pady=10)

# Embed subtitles checkbox
embed_subs_var = tk.BooleanVar()
embed_subs_check = tk.Checkbutton(root, text="Embed Subtitles", variable=embed_subs_var)
embed_subs_check.grid(row=3, column=1, padx=10, pady=10)

# Quality selection
tk.Label(root, text="Quality:").grid(row=4, column=0, padx=10, pady=10)
quality_var = tk.StringVar(value="best")
quality_options = ["best", "worst", "720p", "480p", "360p"]
quality_menu = tk.OptionMenu(root, quality_var, *quality_options)
quality_menu.grid(row=4, column=1, padx=10, pady=10)

# Merge format selection
tk.Label(root, text="Merge Output Format:").grid(row=5, column=0, padx=10, pady=10)
merge_format_var = tk.StringVar(value="mp4")
merge_format_options = ["mp4", "mkv"]
merge_format_menu = tk.OptionMenu(root, merge_format_var, *merge_format_options)
merge_format_menu.grid(row=5, column=1, padx=10, pady=10)

# Video format selection
tk.Label(root, text="Video Format:").grid(row=6, column=0, padx=10, pady=10)
video_format_var = tk.StringVar(value="mp4")
video_format_options = ["mp4", "webm"]
video_format_menu = tk.OptionMenu(root, video_format_var, *video_format_options)
video_format_menu.grid(row=6, column=1, padx=10, pady=10)

# Download button
download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=7, column=1, padx=10, pady=10)

# Log text area
log_text = scrolledtext.ScrolledText(root, width=60, height=15)
log_text.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
