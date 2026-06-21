import threading
import tkinter as tk
from tkinter import filedialog, messagebox

from main import process_video


class VisitorApp:

    def __init__(self, root):

        self.root = root

        root.title(
            "Visitor Analytics System"
        )

        root.geometry("700x500")

        self.video_path = None

        title = tk.Label(
            root,
            text="Visitor Analytics System",
            font=("Arial", 20, "bold")
        )

        title.pack(pady=20)

        self.file_label = tk.Label(
            root,
            text="선택된 영상 없음",
            wraplength=600
        )

        self.file_label.pack(pady=10)

        select_btn = tk.Button(
            root,
            text="동영상 선택",
            width=20,
            command=self.select_video
        )

        select_btn.pack(pady=10)

        analyze_btn = tk.Button(
            root,
            text="분석 시작",
            width=20,
            command=self.start_analysis
        )

        analyze_btn.pack(pady=10)

        self.status_label = tk.Label(
            root,
            text="대기 중"
        )

        self.status_label.pack(pady=10)

        self.result_text = tk.Text(
            root,
            width=70,
            height=15
        )

        self.result_text.pack(pady=10)

    def select_video(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("Video Files",
                 "*.mp4 *.avi *.mov")
            ]
        )

        if path:

            self.video_path = path

            self.file_label.config(
                text=path
            )

    def start_analysis(self):

        if not self.video_path:

            messagebox.showerror(
                "Error",
                "동영상을 선택하세요."
            )

            return

        thread = threading.Thread(
            target=self.run_analysis
        )

        thread.start()

    def run_analysis(self):

        try:

            self.status_label.config(
                text="분석 중..."
            )

            from pathlib import Path

            (
                visitor_count,
                durations,
                output_video
            ) = process_video(
                Path(self.video_path)
            )

            result_lines = []

            result_lines.append(
                f"Total Visitors : {visitor_count}"
            )

            if durations:

                total_time = sum(
                    durations
                )

                avg_time = (
                    total_time /
                    len(durations)
                )

                longest = max(
                    durations
                )

                shortest = min(
                    durations
                )

                result_lines.append("")
                result_lines.append(
                    "SUMMARY"
                )
                result_lines.append(
                    "----------------"
                )

                result_lines.append(
                    f"Average Stay : "
                    f"{avg_time:.1f} sec"
                )

                result_lines.append(
                    f"Longest Stay : "
                    f"{longest:.1f} sec"
                )

                result_lines.append(
                    f"Shortest Stay : "
                    f"{shortest:.1f} sec"
                )

            result_lines.append("")
            result_lines.append(
                f"Result Video:"
            )

            result_lines.append(
                str(output_video)
            )

            self.result_text.delete(
                "1.0",
                tk.END
            )

            self.result_text.insert(
                tk.END,
                "\n".join(result_lines)
            )

            self.status_label.config(
                text="완료"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status_label.config(
                text="오류 발생"
            )


root = tk.Tk()

app = VisitorApp(root)

root.mainloop()