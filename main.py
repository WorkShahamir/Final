import sqlite3
import flet as ft


def init_db():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    location TEXT NOT NULL
                )''')
    events = [
        ('Event 1', '2023-06-10', 'Location 1'),
        ('Event 2', '2023-06-15', 'Location 2'),
        ('Event 3', '2023-06-20', 'Location 3')
    ]
    c.executemany('INSERT INTO events (name, date, location) VALUES (?, ?, ?)', events)
    conn.commit()
    conn.close()


def search_events(query):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute("SELECT name, date, location FROM events WHERE name LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return results


def main(page: ft.Page):
    page.title = "Event Search"
    search_field = ft.TextField(label="Search for an event", on_change=lambda e: update_results(e.control.value))
    results_list = ft.ListView()

    def update_results(query):
        results = search_events(query)
        results_list.controls.clear()
        for event in results:
            results_list.controls.append(ft.Text(f"{event[0]} - {event[1]} - {event[2]}"))
        page.update()

    page.add(search_field, results_list)


if __name__ == "__main__":
    init_db()
    ft.app(target=main)
