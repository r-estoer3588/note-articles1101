import http.server
import socketserver
import json
import csv
import os
import datetime
from urllib.parse import parse_qs

PORT = 8000
DATA_FILE = "monitoring_data.csv"


class MonitoringHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            data = []
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    data = list(reader)

            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/update":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_data = json.loads(post_data.decode("utf-8"))

            self.update_csv(new_data)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"status": "success", "message": "Data updated"}).encode(
                    "utf-8"
                )
            )
        elif self.path == "/api/fetch_x":
            try:
                from x_api_client import fetch_x_data

                result = fetch_x_data()

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_error(500, str(e))

        else:
            self.send_error(404)

    def update_csv(self, entry):
        # Read existing data
        rows = []
        header = [
            "Date",
            "Followers",
            "Followers_Change",
            "Likes",
            "Reposts",
            "Replies",
            "Profile_Clicks",
            "Note_PV",
        ]

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header_row = next(reader, None)
                if header_row:
                    header = header_row
                    rows = list(reader)

        # Prepare new row
        target_date = entry["date"]

        # Calculate change if not provided
        followers = int(entry["followers"])
        followers_change = 0

        # Find index if date exists
        target_index = -1
        for i, row in enumerate(rows):
            if row[0] == target_date:
                target_index = i
                break

        # Calculate change based on previous day
        # Logic: If updating today, compare with yesterday.
        # If adding new day, compare with last entry.

        prev_followers = 0
        # Sort rows by date to ensure correct previous value
        # (Simple string sort works for YYYY-MM-DD)
        sorted_rows = sorted(rows, key=lambda x: x[0])

        # Find the row before the target date
        for row in sorted_rows:
            if row[0] < target_date:
                prev_followers = int(row[1])
            else:
                break

        followers_change = followers - prev_followers

        new_row = [
            target_date,
            str(followers),
            str(followers_change),
            str(entry["likes"]),
            str(entry["reposts"]),
            str(entry["replies"]),
            str(entry["clicks"]),
            str(entry["notepv"]),
        ]

        if target_index != -1:
            rows[target_index] = new_row
        else:
            rows.append(new_row)
            # Re-sort to keep dates in order
            rows.sort(key=lambda x: x[0])

        # Write back
        with open(DATA_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)


print(f"Starting server at http://localhost:{PORT}")
print("Press Ctrl+C to stop.")

with socketserver.TCPServer(("", PORT), MonitoringHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
