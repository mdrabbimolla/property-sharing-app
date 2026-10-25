
import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from PIL import Image, ImageDraw


APP_DIR = os.path.join(
    os.path.expanduser("~"), "property_sharing"
)
os.makedirs(APP_DIR, exist_ok=True)

DB_PATH = os.path.join(APP_DIR, "projects.db")
EXPORT_DIR = os.path.join(APP_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def connect_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            land TEXT,
            flat_size TEXT,
            share_price TEXT,
            phone TEXT,
            details TEXT,
            created_at TEXT
        )
    """)
    con.commit()
    return con


class PropertySharingApp(App):
    def build(self):
        self.title = "Property Sharing"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        root.add_widget(Label(
            text="[b]REAL ESTATE PROJECT SHARING[/b]",
            markup=True,
            font_size="20sp",
            size_hint_y=None,
            height=dp(48)
        ))

        self.fields = {}
        field_names = [
            ("name", "Project name *"),
            ("location", "Project location"),
            ("land", "Land size, e.g. 20 Katha"),
            ("flat_size", "Flat size, e.g. 1638 sq ft"),
            ("share_price", "Share price, e.g. 28 lakh"),
            ("phone", "Contact phone"),
            ("details", "Project details")
        ]

        for key, hint in field_names:
            box = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(53)
            )
            field = TextInput(
                hint_text=hint,
                multiline=(key == "details"),
                size_hint_y=1
            )
            self.fields[key] = field
            box.add_widget(field)
            root.add_widget(box)

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(6)
        )

        add_btn = Button(text="Save Project")
        add_btn.bind(on_release=self.save_project)
        buttons.add_widget(add_btn)

        list_btn = Button(text="Show Projects")
        list_btn.bind(on_release=self.show_projects)
        buttons.add_widget(list_btn)

        root.add_widget(buttons)

        self.status = Label(
            text="Add a new real estate project.",
            size_hint_y=None,
            height=dp(48)
        )
        root.add_widget(self.status)

        self.project_area = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None
        )
        self.project_area.bind(
            minimum_height=self.project_area.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.project_area)
        root.add_widget(scroll)

        connect_db().close()
        self.show_projects()
        return root

    def save_project(self, *_):
        data = {
            key: widget.text.strip()
            for key, widget in self.fields.items()
        }

        if not data["name"]:
            self.status.text = "Project name is required."
            return

        con = connect_db()
        con.execute("""
            INSERT INTO projects
            (name, location, land, flat_size, share_price,
             phone, details, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"], data["location"], data["land"],
            data["flat_size"], data["share_price"],
            data["phone"], data["details"],
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))
        con.commit()
        con.close()

        for widget in self.fields.values():
            widget.text = ""

        self.status.text = "Project saved successfully."
        self.show_projects()

    def show_projects(self, *_):
        self.project_area.clear_widgets()

        con = connect_db()
        projects = con.execute("""
            SELECT id, name, location, land, flat_size,
                   share_price, phone, details
            FROM projects ORDER BY id DESC
        """).fetchall()
        con.close()

        if not projects:
            self.project_area.add_widget(Label(
                text="No projects yet. Add your first project.",
                size_hint_y=None,
                height=dp(50)
            ))
            return

        for project in projects:
            pid, name, location, land, flat_size, price, phone, details = project

            card = BoxLayout(
                orientation="vertical",
                padding=dp(8),
                spacing=dp(5),
                size_hint_y=None,
                height=dp(230)
            )

            card.add_widget(Label(
                text=f"[b]{name}[/b]",
                markup=True,
                size_hint_y=None,
                height=dp(35)
            ))

            card.add_widget(Label(
                text=(
                    f"Location: {location or '-'}\n"
                    f"Land: {land or '-'} | Flat: {flat_size or '-'}\n"
                    f"Share price: {price or '-'}\n"
                    f"Contact: {phone or '-'}"
                ),
                size_hint_y=None,
                height=dp(85)
            ))

            actions = BoxLayout(
                size_hint_y=None,
                height=dp(42),
                spacing=dp(5)
            )

            jpg_btn = Button(text="Create JPEG")
            jpg_btn.bind(
                on_release=lambda _, p=project: self.make_jpeg(p)
            )
            actions.add_widget(jpg_btn)

            pdf_btn = Button(text="Create PDF")
            pdf_btn.bind(
                on_release=lambda _, p=project: self.make_pdf(p)
            )
            actions.add_widget(pdf_btn)

            del_btn = Button(text="Delete")
            del_btn.bind(
                on_release=lambda _, project_id=pid:
                self.delete_project(project_id)
            )
            actions.add_widget(del_btn)

            card.add_widget(actions)
            self.project_area.add_widget(card)

    def project_text(self, p):
        _, name, location, land, flat_size, price, phone, details = p
        return (
            f"{name}\n\n"
            f"Location: {location or '-'}\n"
            f"Land: {land or '-'}\n"
            f"Flat size: {flat_size or '-'}\n"
            f"Share price: {price or '-'}\n"
            f"Contact: {phone or '-'}\n\n"
            f"Details:\n{details or '-'}"
        )

    def make_jpeg(self, p):
        text = self.project_text(p)
        img = Image.new("RGB", (1080, 1350), "#f3f5f8")
        draw = ImageDraw.Draw(img)

        draw.rectangle((0, 0, 1080, 210), fill="#102b46")
        draw.text(
            (55, 65), "REAL ESTATE PROJECT",
            fill="white", stroke_width=0
        )

        y = 270
        for line in text.splitlines():
            if y > 1260:
                break
            draw.text((55, y), line[:75], fill="#172b3c")
            y += 48

        filename = os.path.join(
            EXPORT_DIR, f"project_{p[0]}.jpg"
        )
        img.save(filename, "JPEG", quality=92)
        self.status.text = f"JPEG created: {filename}"

    def make_pdf(self, p):
        """Create a small PDF using Python's standard library only."""
        import textwrap

        filename = os.path.join(
            EXPORT_DIR, f"project_{p[0]}.pdf"
        )

        def pdf_text(value):
            # Built-in PDF Helvetica supports WinAnsi/ASCII, not Bengali fonts.
            # Keep the PDF valid even when a field contains unsupported glyphs.
            value = str(value).encode("ascii", "replace").decode("ascii")
            return value.replace("\\\\", "\\\\\\\\").replace("(", "\\\\(").replace(")", "\\\\)")

        lines = []
        for raw in self.project_text(p).splitlines():
            if not raw:
                lines.append("")
            else:
                lines.extend(textwrap.wrap(raw, width=82) or [""])

        # Split content across A4 pages, leaving room for the heading.
        page_lines = []
        current = []
        for line in lines:
            if len(current) >= 38:
                page_lines.append(current)
                current = []
            current.append(line)
        if current or not page_lines:
            page_lines.append(current)

        objects = []
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        page_refs = [f"{4 + i * 2} 0 R" for i in range(len(page_lines))]
        objects.append(
            ("<< /Type /Pages /Kids [" + " ".join(page_refs) +
             f"] /Count {len(page_lines)} >>").encode("ascii")
        )
        objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

        for page_index, lines_on_page in enumerate(page_lines):
            page_obj_num = 4 + page_index * 2
            content_obj_num = page_obj_num + 1
            commands = [
                "q 0.06 0.17 0.27 rg 0 747 595 95 re f Q",
                "BT /F1 19 Tf 42 785 Td (REAL ESTATE PROJECT) Tj ET",
                "BT /F1 11 Tf 42 715 Td 16 TL"
            ]
            for line in lines_on_page:
                commands.append(f"({pdf_text(line)}) Tj T*")
            commands.append("ET")
            stream = ("\n".join(commands) + "\n").encode("ascii", "replace")
            page_obj = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_obj_num} 0 R >>"
            ).encode("ascii")
            content_obj = (
                f"<< /Length {len(stream)} >>\nstream\n".encode("ascii")
                + stream + b"endstream"
            )
            objects.extend([page_obj, content_obj])

        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for number, obj in enumerate(objects, start=1):
            offsets.append(len(output))
            output.extend(f"{number} 0 obj\n".encode("ascii"))
            output.extend(obj)
            output.extend(b"\nendobj\n")

        xref_offset = len(output)
        output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
        output.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
        output.extend(
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
        )

        with open(filename, "wb") as pdf_file:
            pdf_file.write(output)
        self.status.text = f"PDF created: {filename}"

    def delete_project(self, project_id):
        con = connect_db()
        con.execute("DELETE FROM projects WHERE id=?", (project_id,))
        con.commit()
        con.close()
        self.status.text = "Project deleted."
        self.show_projects()


if __name__ == "__main__":
    PropertySharingApp().run()
