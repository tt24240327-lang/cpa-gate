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
    1.  **Synchronous Notification (Critical):**
        *   Upon detecting a human user, the system **Synchronously** sends a Telegram alert (`💰 [Keyword] 유입`).
        *   **[NEW] Google Analytics Reporting:** Sends a server-side hit to GA4 (`G-1VH7D6BJTD`) with the event `CPA_Click`, including parameters for `keyword` and `vendor`.
        *   The system *waits* for these API calls to ensure tracking is recorded before the user leaves.
    2.  **Dual Target Selection (A/B):**
        *   Checks `t` parameter (`t=A` for ReplyAlba, `t=B` for AlbaRich).
    3.  **Direct Redirect (Final Action):**
        *   Once the Telegram message is confirmed sent, the system returns a **302 Redirect** response.
        *   The user is immediately moved to the official target landing page.
        *   (Proxying was removed to prevent 'White Screen' blocking issues).

---

## 📊 3. Data & Configuration (데이터 및 설정)

### Global Variables
*   **`GA_MEASUREMENT_ID` (New):** `G-1VH7D6BJTD`
    *   Used for server-side Google Analytics tracking via Measurement Protocol.
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

## 🛡️ 5. Anti-Fingerprinting & Stealth Protocol (보안 및 지문 삭제)
To prevent "Clone Site" detection by Naver Yeti/Google Bots, the following randomization features are enforced:

### 1. Footer & Business Info Randomization
*   **Objective:** No two domains share the same footer info.
*   **Implementation:**
    *   **Locations:** Random selection from major tech hubs (Gangnam, Pangyo, Haeundae, Songdo, etc.).
    *   **Biz Number:** Generated pattern `XXX-XX-XXXXX` seeded by domain.
    *   **Text Variance:** Privacy policy and terms links use varied phrasings (e.g., '개인정보처리방침', 'Privacy', '정보보호정책').

### 2. Code Obfuscation (CSS/HTML)
*   **Objective:** Eliminate structural footprints.
*   **Implementation:**
    *   **Class Names:** Instead of fixed names like `.nav`, the system generates seeded class names (e.g., `.nav-8f2`, `.wrap-b21`).
    *   **Structure:** Layouts (A/B/C/D) provide structural diversity.

### 3. Metadata & Asset Variation
*   **Favicons:** Geometrically generated SVGs specific to the domain hash.
*   **Meta Tags:** Descriptions and OG tags are assembled from random fragments to avoid duplication.

### 4. Tracking Isolation
*   **GA4:** Supports server-side injection (`send_ga_event`) which hides the tracking ID from the client-side source code (unless specifically exposed).
*   **Isolation:** Each deployment can theoretically hold different tracking IDs via environment variables.

---
**This document serves as the master blueprint. Any modifications should respect this 3-part structure.**
