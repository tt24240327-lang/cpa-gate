# FINAL_SYSTEM_STRUCTURE.md (Empire Genesis-AI System Architecture)

## 🏗️ 1. System Overview (시스템 개요)
This system is designed as a **Hybrid-Camouflage System** that behaves differently depending on who accesses it.
*   **For Bots (SEO):** It presents itself as a legitimate "Data Science / Technology Institute."
*   **For Humans (CPA):** It acts as a mirror/proxy for designated CPA landing pages (A/B Target).

---

## 🔒 2. System Components (3-Part Structure)

### [Part 1] Security Check & Traffic Control (보안 검문소)
*   **Purpose:** Filters malicious traffic, identifies Bots vs Humans, and blocks hackers.
*   **Location:** `api/index.py` (Lines 453 - 483)
*   **Key Functions:**
    *   **Fingerprinting:** Generates unique ID (`f_print`) for every visitor (Line 458).
    *   **Cyber Jail (G_JAIL):** Blocks IPs attempting to access forbidden paths (`.env`, `admin`) (Lines 464-469).
    *   **Bot Detection:** Checks User-Agent for signals (`naver`, `bot`, `yeti`) (Line 473).
    *   **Routing Decision:**
        *   **If Bot or No Key (`k`):** Send to **[Part 2]**.
        *   **If Human with Key (`k`):** Send to **[Part 3]**.

### [Part 2] GeneEngine: The Camouflage Factory (가짜 공장)
*   **Purpose:** Generates high-quality, professional-looking "Tech Company" content for SEO bots.
*   **Location:** `api/index.py` (Lines 266 - 430)
*   **Features:**
    *   **Dynamic Identity:** Uses the domain name (e.g., `link-us`) to deterministically generate a unique logo, color theme, and company name (Lines 270-272).
    *   **Multi-Layout System:** Randomly selects between 4 layouts (Enterprise, Portal, Dashboard, Startup) (Lines 125-263).
    *   **Content Generation:** Generates fake but realistic content for Network, Security, and Data pages to satisfy crawl bots.
    *   **Error Handling:** Handles 404s or invalid paths by showing a "System Status" or "Data Warehouse" page, ensuring bots never see a broken page.

### [Part 3] CPA Proxy: The Real Store (진짜 매장)
*   **Purpose:** Monetization via CPA landing pages.
*   **Location:** `api/index.py` (Lines 487 - 527)
*   **Workflow:**
    1.  **Notification:** Sends a Telegram alert (`💰 [Keyword] 유입`) upon human entry (Lines 501-502).
    2.  **Dual Target Selection (A/B):**
        *   Checks `t` parameter.
        *   `t=A` (Default) -> **ReplyAlba (이사방)**
        *   `t=B` -> **AlbaRich (모두클린)**
        *   (Lines 504-513)
    3.  **Proxy Mirroring:**
        *   Fetches the actual content from the Target URL.
        *   Rewrites internal links (`src`, `href`) to proxy through our domain (Line 520).
        *   **Direct Form Submission:** Allows users to submit forms directly to the Target server (Line 521 is commented out to enable this).

---

## 📊 3. Data & Configuration (데이터 및 설정)

### Global Variables
*   **`CPA_DATA` (Lines 24-55):** The central mapping table.
    *   Format: `Key (Hash)`: [`Keyword`, `Code A (ReplyAlba)`, `Code B (AlbaRich)`]
    *   Example: `"8cf12edf": ["이사청소", "WwVCgW9E1R", "z2NytCt42i"]`
*   **`TARGET_A` / `TARGET_B` (Lines 57-58):**
    *   `TARGET_A`: `https://replyalba.co.kr` (Primary)
    *   `TARGET_B`: `https://albarich.com` (Secondary)

### Security Sets
*   **`G_JAIL`:** An in-memory set of banned fingerprints (IP + UserAgent).
*   **`FORBIDDEN_PATHS`:** List of dangerous paths (e.g., `admin`, `.env`) that trigger an immediate ban.

---

## 🔧 4. Critical Logic Chains (핵심 로직 연결)

1.  **Seed consistency (Lines 270-272):**
    *   `host.replace("www.", "").split('.')[0]`
    *   Ensures `abc.shop` and `abc.xyz` look identical.

2.  **Dual Target Routing (Lines 508-513):**
    *   `if t_param == 'B': code_idx = 2`
    *   `else: code_idx = 1`
    *   Uses `CPA_DATA` index to pick the correct affiliate code.

3.  **Telegram Logic (Lines 435-437):**
    *   Asynchronous-like (short timeout) POST request to prevent slowing down the user experience.

---

## ⚠️ Known Issues & Fixes (FIX LOG)
*   [FIXED] **404 Error on CPA Pages:** Caused by relative paths (e.g., `intro/md_clean`) being appended to Target URLs.
    *   **Solution:** Force the Target URL to be the absolute path `/pt/{code}` when a valid `k` is present, ignoring any garbage path. (Implemented in lines 515).
*   [FIXED] **Form Submission:** Originally intercepted by `/api/capture`.
    *   **Solution:** Commented out interception (Line 521) to allow direct POST to affiliate providers.

---
**This document serves as the master blueprint. Any modifications should respect this 3-part structure.**
