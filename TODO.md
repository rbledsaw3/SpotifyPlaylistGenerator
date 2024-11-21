# TODO

This document outlines future improvements and enhancements planned for the **Spotify Playlist Creator** project.

---

## 🎯 **Planned Features**

### 1. **Playlist Name Abstraction**
   - **Goal:** Remove hardcoded playlist name patterns to make the project more flexible for users.
   - **Details:**
     - Allow users to define custom playlist naming conventions via configuration or CLI arguments.
     - Support template-based names (e.g., `Top {Year}` or `{Year} - {Type}`).
   - **Status:** Not started.

---

### 2. **Asynchronous Requests**
   - **Goal:** Improve speed by handling API requests asynchronously.
   - **Details:**
     - Rewrite API calls to support parallel requests (e.g., searching for songs or adding tracks to playlists).
     - Consider using libraries like `asyncio` in Python or rewriting the project in Go or NodeJS.
     - Ensure error handling and rate-limiting are robust in an asynchronous context.
   - **Status:** Not started.

---

### 3. **More Robust Error Handling**
   - **Goal:** Expand error handling to cover a wider range of HTTP status codes.
   - **Details:**
     - Handle 4xx errors (e.g., 400 Bad Request, 404 Not Found) with appropriate fallbacks.
     - Handle 5xx errors (e.g., 500 Internal Server Error) with retry logic.
     - Log errors to a file for debugging.
   - **Status:** Not started.

---

### 4. **Support Other Data Formats**
   - **Goal:** Allow the project to handle playlist data in formats beyond JSON.
   - **Details:**
     - Add support for:
       - **XML:** Exported from iTunes.
       - **M3U:** For legacy WinAmp playlists.
       - **WPL:** For Windows Media Player.
     - Automatically detect file format based on file extension or user input.
     - Provide conversion tools if necessary.
   - **Status:** Not started.

---

## 🛠 **Refactoring and Cleanup**

- Modularize the code further to make it easier to test and extend.
- Add detailed comments and docstrings to improve maintainability.
- Improve test coverage:
  - Add tests for error handling.
  - Add tests for new file formats (XML, M3U, WPL).

---

## 💡 **Ideas for the Future**
- **CLI Improvements:** Add more options for command-line customization.
- **Docker Support:** Create a Docker container for easier setup and usage.
