import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from recommendation import get_recommendations


INTERESTS = [
    "Programming", "Problem Solving", "Technology", "Data",
    "Cybersecurity", "Electronics", "Robotics", "Machines",
    "Design", "Creativity", "Artificial Intelligence",
    "Business", "Communication"
]

SKILLS = [
    "Python", "Java", "C", "Excel", "Statistics", "Networking",
    "Circuit Design", "CAD", "Figma", "Problem Solving",
    "Creativity", "Communication", "Mathematics", "Data Analysis"
]

SUBJECTS = [
    "Computer Science", "Mathematics", "Physics", "Electronics",
    "Statistics", "Design", "Business Studies", "English"
]


class CareerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Career Recommendation System")
        self.root.geometry("900x760")
        self.root.minsize(760, 650)
        self.root.configure(bg="#f2f5fa")
        self.last_report = ""

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10), padding=7)
        style.configure("TLabelframe", background="#ffffff")
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
        style.configure("TLabel", background="#ffffff", font=("Arial", 10))

        header = tk.Frame(root, bg="#172b4d", pady=18)
        header.pack(fill="x")
        tk.Label(
            header, text="CAREER RECOMMENDATION SYSTEM",
            font=("Arial", 19, "bold"), fg="white", bg="#172b4d"
        ).pack()
        tk.Label(
            header, text="Discover career paths based on your interests and skills",
            font=("Arial", 10), fg="#dce6f5", bg="#172b4d"
        ).pack(pady=(5, 0))

        content = tk.Frame(root, bg="#f2f5fa", padx=18, pady=14)
        content.pack(fill="both", expand=True)

        name_frame = ttk.LabelFrame(content, text="Student Details", padding=10)
        name_frame.pack(fill="x", pady=5)
        ttk.Label(name_frame, text="Student name:").pack(side="left")
        self.name_entry = ttk.Entry(name_frame, width=35)
        self.name_entry.pack(side="left", padx=10)

        selection_frame = tk.Frame(content, bg="#f2f5fa")
        selection_frame.pack(fill="both", expand=True, pady=8)

        self.interest_box = self.create_list(
            selection_frame, "Choose Your Interests", INTERESTS, 0, 0
        )
        self.skill_box = self.create_list(
            selection_frame, "Choose Your Skills", SKILLS, 0, 1
        )
        self.subject_box = self.create_list(
            selection_frame, "Choose Favourite Subjects", SUBJECTS, 1, 0
        )

        button_frame = tk.Frame(content, bg="#f2f5fa")
        button_frame.pack(fill="x", pady=8)

        ttk.Button(
            button_frame, text="Get Recommendations",
            command=self.show_recommendations
        ).pack(side="left", padx=4)

        ttk.Button(
            button_frame, text="Save Report",
            command=self.save_report
        ).pack(side="left", padx=4)

        ttk.Button(
            button_frame, text="Clear",
            command=self.clear_form
        ).pack(side="left", padx=4)

        result_frame = ttk.LabelFrame(content, text="Career Recommendations", padding=10)
        result_frame.pack(fill="both", expand=True, pady=5)

        self.result_text = tk.Text(
            result_frame, height=12, wrap="word",
            font=("Arial", 10), bg="white", relief="flat",
            padx=10, pady=10
        )
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert(
            "1.0", "Your career recommendations will appear here.\n"
        )
        self.result_text.config(state="disabled")

    def create_list(self, parent, title, options, row, column):
        frame = ttk.LabelFrame(parent, text=title, padding=8)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        box = tk.Listbox(
            frame, selectmode=tk.MULTIPLE, height=7,
            exportselection=False, font=("Arial", 10)
        )
        for option in options:
            box.insert(tk.END, option)
        box.pack(fill="both", expand=True)
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        return box

    def selected_items(self, listbox):
        return [listbox.get(i) for i in listbox.curselection()]

    def show_recommendations(self):
        name = self.name_entry.get().strip()
        interests = self.selected_items(self.interest_box)
        skills = self.selected_items(self.skill_box)
        subjects = self.selected_items(self.subject_box)

        if not name:
            messagebox.showwarning("Missing Details", "Please enter your name.")
            return

        if not (interests or skills or subjects):
            messagebox.showwarning(
                "Missing Choices", "Please select at least one interest, skill or subject."
            )
            return

        recommendations = get_recommendations(interests, skills, subjects)

        lines = [
            "CAREER RECOMMENDATION REPORT",
            "=" * 48,
            f"Student: {name}",
            f"Interests: {', '.join(interests) if interests else 'Not selected'}",
            f"Skills: {', '.join(skills) if skills else 'Not selected'}",
            f"Subjects: {', '.join(subjects) if subjects else 'Not selected'}",
            "",
        ]

        if not recommendations:
            lines.append("No matching careers found. Try selecting more options.")
        else:
            lines.append("Your best matches:")
            lines.append("")
            for number, career in enumerate(recommendations[:5], start=1):
                lines.extend([
                    f"{number}. {career['title']} - {career['score']}% match",
                    career["description"],
                    f"Matched interests: {', '.join(career['matched_interests']) or 'None'}",
                    f"Matched skills: {', '.join(career['matched_skills']) or 'None'}",
                    f"Matched subjects: {', '.join(career['matched_subjects']) or 'None'}",
                    "-" * 48,
                ])

        lines.extend([
            "",
            "Note: Scores are simple rule-based matches, not a guarantee",
            "of career suitability. Explore each field before deciding."
        ])

        self.last_report = "\n".join(lines)
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", self.last_report)
        self.result_text.config(state="disabled")

    def save_report(self):
        if not self.last_report:
            messagebox.showinfo(
                "No Report", "Generate career recommendations before saving."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            initialfile="career_report.txt"
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.last_report)
                messagebox.showinfo("Saved", "Your report was saved successfully.")
            except OSError as error:
                messagebox.showerror("Save Error", str(error))

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        for box in (self.interest_box, self.skill_box, self.subject_box):
            box.selection_clear(0, tk.END)
        self.last_report = ""
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", "Your career recommendations will appear here.\n")
        self.result_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = CareerApp(root)
    root.mainloop()
