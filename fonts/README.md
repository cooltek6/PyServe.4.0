Place any custom TTF fonts you want to bundle with this project in this folder.

Recommended filename for Ubuntu Sans Medium (if you include it):
  Ubuntu-M.ttf

The application will attempt to detect system fonts first. If you want to force a bundled font, set `pdf_font_path` when creating a `ServiceOrderForm` (or drop a TTF here and update the code to prefer the project `fonts/` directory).