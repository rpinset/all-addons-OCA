This module extends the report configuration in order to display HTML content inside Report Footer on chosen reports.

### Implementation Details

The footer is injected into various report layouts. In some cases, the native footer div is **replaced** instead of just adding content before it:

- **`Bubble`**: The div is replaced to move the vertical separator bar that splits the footer content, ensuring a clean layout with the custom footer displayed above the native one.

- **`Standard`, `Folder`, `Boxed` and `Bold`**: The div is replaced and the footer layout is modified to ensure the HTML footer content occupies the full width instead of appearing inline with other elements.

In other layouts (`striped`, `wave`), the custom footer is simply inserted before the native footer without replacing it, as the layout structure handles the distribution correctly.