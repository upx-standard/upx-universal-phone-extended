# UPX — Universal Phone eXtended  
**An open, modular hardware standard for smartphones**  
**Version:** v0.2‑draft — 2025‑09‑25  
**Author:** Matteo & the community  
**Spec License (proposal):** CERN‑OHL‑P v2 (permissive, open hardware)  
**Reference code license:** Apache‑2.0

## Abstract
**UPX** is a vendor‑neutral **hardware standard** for modular smartphones — the smartphone equivalent of **ATX** for PCs. It defines **mechanical bays**, **electrical interfaces**, and a thin **software abstraction** so that anyone can mix and match: **compute modules, displays, cameras, batteries, radios, sensors, and accessories**.

UPX is **OS‑agnostic**: any OS that implements the UPX HAL can run (Linux first, with Android compatibility via containerization such as Waydroid).  
UPX is **case‑agnostic**: any enclosure or industrial design can be used, as long as the **internal mount grid, keep‑out zones, and connectors** are respected.  
UPX is **module‑agnostic**: from simple sensors to high‑power accessories — even unusual ones. A **Safety & Permissions model** governs risky modules.

UPX is not a single product. It is a **shared language and test suite** that lets communities and manufacturers build a sustainable, repairable, privacy‑respecting phone ecosystem.

## 1) Problem & Vision
Phones today are sealed black boxes: locked boot chains, short support windows, fragile repairs, zero upgrade paths, and vendor lock‑in. Developers and users alike are forced into two walled gardens.
**UPX flips this:** open interfaces, replaceable modules, owner control, and long‑term serviceability — with a standard strong enough that multiple vendors can interoperate and compete.

## 2) Scope & Non‑Goals
**In scope**
- Mechanical envelopes and **bay geometry** for modules.
- Electrical interfaces: **power rails, high‑speed lanes, control buses**.
- A minimal **UPX HAL** (hardware abstraction) and **Module Manifest** format.
- **Compliance levels** and an **Open Test Suite (OTS)**.

**Out of scope**
- Dictating a single SoC vendor or a single OS.
- Mandating a specific case material or aesthetics.
- Providing a turnkey modem stack (OEMs choose, standard provides hooks).

## 3) Design Principles
- **Open & neutral:** royalty‑free, public spec, community governance.  
- **Realistic:** builds on widely used tech (MIPI‑DSI/CSI, USB‑C, PCIe, I²C, SPI).  
- **Modular & repairable:** core subsystems are replaceable, not glued monoliths.  
- **Security with owner control:** verified boot is allowed, but **keys belong to the owner**.  
- **Long‑lived:** mechanical and electrical margins for multiple generations.  
- **Performance‑agnostic:** same sockets from low‑power to enthusiast builds.  
- **OS‑agnostic:** any OS can implement UPX HAL; spec never hardcodes a distro.

## 4) System Overview
UPX defines **module classes** and how they connect:
- **UPX‑CM** — *Compute Module* (SoC, RAM, storage controller, Wi‑Fi/BT optional).  
- **UPX‑RFM** — *Radio/Modem Module* (4G/5G, eSIM/SIM, GNSS).  
- **UPX‑DM** — *Display Module* (Panel + Touch via MIPI‑DSI + I²C).  
- **UPX‑CAM** — *Camera Module* (MIPI‑CSI‑2).  
- **UPX‑EPM** — *Energy & Power Module* (battery pack, charger/PMIC, fuel gauge).  
- **UPX‑AUX** — *Aux/Expansion Modules* (audio, sensors, keyboards, grips, etc.).  
Core modules mate to the **UPX‑Edge Connector** (mezzanine, high‑speed) on a thin **Backplane**. External accessories can use a **Pogo Accessory Rail**.

## 5) Mechanics (v0.2 proposal)
**Device Envelopes** (examples, not exclusive):
- **UPX‑A (Compact):** 152 × 75 × 8.5 mm  
- **UPX‑B (Standard):** 162 × 78 × 9.0 mm  
- **UPX‑C (Large):** 170 × 80 × 9.5 mm

**Internal Mount Grid & Bays**
- **Compute Bay:** 40 × 30 mm, 4× M1.6 standoffs, max z‑height 2.8 mm (both sides).  
- **Battery Bay:** freeform area; standardized **EPM Pogo** zone.  
- **Camera Bays:** 12 × 12 mm (Prime), optional secondary bays.  
- **Accessory Rail:** 6‑pin pogo strip along edge or rear (for grips, lenses, sleds).
**Case‑agnostic by design:** any enclosure (3D‑printed, CNC’d, polymer, aluminum) is allowed if the **mount grid**, **keep‑out volumes**, and **connector locations** are respected.

## 6) Electrical Interfaces (v0.2 proposal)
### 6.1 UPX‑Edge Connector (CM ↔ Backplane)
Type: board‑to‑board mezzanine, ≤0.4 mm pitch, **~120 pins** (two rows).  
Groups (indicative; final pin map in Annex A):
- **Power rails:** `SYS_BAT` (3.0–4.4 V), optional `VSYS_5V`, `3V3_AUX`, `1V8_AUX`.  
- **High‑speed lanes:** MIPI‑DSI (up to 4 lanes), MIPI‑CSI‑2 (up to 2× 4 lanes), **PCIe x1/x2**, **USB 3.x**, USB 2.0, SDIO.  
- **Control buses:** I²C (x2), SPI (x2), UART (x2), GPIOs, PWM, IRQ.  
- **Audio:** I²S/TDM, DMIC, HP detect.  
- **Debug & misc:** Reset, BootSel, Wake, Debug UART, SWD/JTAG.
> Reserve ground and return pins are interleaved for SI/EMI. Differential pairs length‑matched.

### 6.2 Power (UPX‑EPM)
Primary rail `SYS_BAT` from Li‑ion pack; **USB‑C PD** input supported.  
EPM integrates **charger/PMIC**, **fuel gauge**, **thermal sensors**, and **hardware protections** (fuses, OVP/UVP).  
Backplane measures current and temperature; firmware can **derate** or **cut off**.

### 6.3 Display (UPX‑DM)
**MIPI‑DSI** up to 4 lanes; touch over I²C.  
Standardized **panel FPC** pinout family (Annex B).

### 6.4 Camera (UPX‑CAM)
**MIPI‑CSI‑2** up to 4 lanes per camera bay.  
Optional lens interchangeability; camera EEPROM stores calibration.

### 6.5 Radio (UPX‑RFM)
Modular modem via **PCIe or USB 3.x** + I²C control; eSIM + optional dual nano‑SIM.  
RF via u.FL to case antennas.

### 6.6 Expansion (UPX‑AUX / UPX‑XP)
Generic **Expansion Profile (UPX‑XP)** offering:
- One high‑speed path (**PCIe x1** or **USB 3.x**) when needed.  
- Low‑speed control (**I²C/SPI/UART**, PWM, GPIO, optional ADC).  
- Declared **power budget** per module; backplane enforcement.

## 7) Software & OS‑Agnostic HAL
**UPX does not pick an OS.** Any OS can run if it implements:
- **UPX HAL**: a thin abstraction over standard Linux interfaces (I²C/SPI/UART/GPIO/PCIe/USB).  
- **UPX Module Manifest**: each module exposes a small self‑description (EEPROM or virtual) with vendor ID, product ID, capabilities, power profile, and required drivers.  
- **upx‑agent** (userspace): enumerates modules, handles firmware updates, enforces permissions/safety policies, and exposes a clean API to higher layers.
**Android compatibility** is delivered via containerization (e.g., **Waydroid**) with GPU acceleration where available. Nothing in UPX requires Google services.

## 8) Boot, Ownership & Security
- **Open boot path**: ROM → SPL → U‑Boot → Linux; measured/verified boot optional.  
- **Owner‑controlled keys**: verified boot can be enabled, but the device owner controls the trust anchors.  
- **Recovery**: physical combo to enter recovery/DFU; flash without vendor permission.  
- **Module signing** (optional but recommended): firmware blobs signed by module maker; upx‑agent can require signatures for higher compliance levels.

## 9) Safety & Permissions (critical for “anything modules”)
UPX explicitly supports **unusual or high‑risk modules** (industrial sensors, lab gear, high‑power tools) — but under a strict **Safety & Permissions** framework:
- Every module declares a **Safety Class** (e.g., Basic, Elevated, Hazardous).  
- The OS must request **explicit owner consent** to enable Elevated/Hazardous modules.  
- **Hardware interlocks** (where applicable) must be satisfied before power‑up.  
- Backplane can **hard‑cut** power on fault or thermal events.  
- Consumer devices may **forbid** certain classes unless the device is a **DevKit**.
See **Annex D** for an illustrative Laser Module (concept).

## 10) Compatibility Levels (device badges)
- **L0 — DevKit:** lab‑friendly, debug headers visible, all module classes enabled with owner overrides.  
- **L1 — Core:** display/touch, Wi‑Fi/BT, battery, camera, USB‑C; no cellular.  
- **L2 — Cellular Basic:** adds 4G + GNSS.  
- **L3 — Cellular Advanced:** 5G Sub‑6, dual cam, high‑refresh panel.  
- **L4 — Pro:** optional mmWave, PCIe expansion, higher thermal headroom.
Vendors may claim **“UPX‑Compatible Lx”** after passing the **Open Test Suite (OTS)**.

## 11) Thermals & Power Budgets
- Typical **Compute Module** sustained power: 3–7 W; short bursts higher.  
- Heat spread via graphite/vapor chamber into the rear shell.  
- Charging derates automatically at elevated pack temperature.

## 12) Reference Path (practical first steps)
- **UPX DevKit‑Zero**: Backplane + Edge connector; compute based on available community modules (e.g., Rockchip or RISC‑V compute boards), 1080p panel, single camera, USB‑C PD, ~5000 mAh pack, 3D‑printable case.  
- **UPX Reference Phone‑A**: L2 target with dual camera, 120 Hz panel, PCIe storage; mainline‑first kernel where possible, Waydroid demo.
> Qualcomm Snapdragon parts are rarely obtainable for indie teams. Start with well‑documented ARM/RISC‑V modules and move upward as partners join.

## 13) Governance & Licensing
- **UPX Working Group (UPX‑WG)**: open technical steering (community + vendors).  
- **Spec license:** **CERN‑OHL‑P v2** (open hardware, permissive).  
- **Code license:** **Apache‑2.0**.  
- **Trademark:** “UPX‑Compatible” usable after passing OTS; lightweight, transparent process.

## 14) Monetization (optional, neutral)
- Sell **reference devices** and **developer kits**.  
- Offer **certification/testing** and long‑term security backports.  
- Build an ecosystem of **accessories and modules** (third‑party friendly).  
- Enterprise options: **documentation, SBOMs, security SLAs**.

## 15) Roadmap (indicative)
- **2025 Q4:** Publish spec v0.2‑draft, repo, logo, website, community kickoff.  
- **2026 Q1:** DevKit‑Zero schematics + bring‑up (display/touch).  
- **2026 Q2:** Camera + EPM integration; Waydroid GPU path.  
- **2026 Q3:** Reference Phone‑A EVT; OTS v0.1; “UPX‑Compatible L2”.  
- **2026 Q4:** DVT/Beta, partner samples (Pine64/Framework/Fairphone outreach).  
- **2027:** First market devices by community/OEMs.

## 16) Prior Art & Why UPX is different
- **Fairphone / PinePhone / Librem 5:** repairable/open, but no shared, vendor‑neutral **form‑factor standard**.  
- **Project Ara:** radical granularity, but mechanically/economically fragile.  
- **UPX** picks a **pragmatic middle**: a few strong interfaces + clear bays → feasible today.

## 17) Privacy Defaults
- No Google Play Services by default; F‑Droid/alt stores supported.  
- Sandboxing (SELinux/AppArmor), verified system partitions.  
- Local‑first options (on‑device AI if NPUs exist).

## 18) Sustainability & Repair
- Batteries are **replaceable** (EPM pogo) and documented.  
- Parts lists and service manuals released where possible.  
- RoHS/REACH minded; conflict‑minerals transparency encouraged.

## 19) Publishing, Assets & Community
- Git repo structure:  
  - `/spec` (this whitepaper + pin maps)  
  - `/ref-design` (schematics, PCB, CAD)  
  - `/tools/ots` (Open Test Suite)  
  - `/docs` (HAL, manifests, driver notes)
- Public chat (Matrix/Discord), issue tracker, weekly community call.

## 20) Call to Action
**UPX is not a product. It is a starting point.**  
If you build hardware, patch kernels, design CAD, or just want a phone you actually own:
- Contribute to the spec, pin maps, and DevKit‑Zero.  
- Propose a module or case.  
- Help us shape the test suite.
Let’s make smartphones as open and diverse as PCs — just smaller.

## Annex A — Indicative UPX‑Edge Map (v0.2 snapshot)
A ~120‑pin mezzanine with:
- **Power:** `SYS_BAT`, `VSYS_5V` (optional), `3V3_AUX`, `1V8_AUX`, abundant GND.  
- **Display:** up to 4‑lane MIPI‑DSI + I²C for touch/backlight.  
- **Camera:** up to two MIPI‑CSI‑2 ports (4 lanes each).  
- **High‑speed general:** one **USB 3.x**, one or two **PCIe x1** (or x2), USB 2.0, SDIO.  
- **Control:** I²C×2, SPI×2, UART×2, GPIO bank, PWM, IRQ lines.  
- **Debug/misc:** Debug UART, SWD/JTAG mux, Reset, BootSel, Wake.
(Exact lane assignment finalized with signal‑integrity review; ground fencing between pairs.)

## Annex B — Display FPC Family (outline)
- MIPI‑DSI 4‑lane variants with I²C for touch.  
- Standardized connector pitches and pin families (30–40 pins).  
- Required EEPROM field: panel ID + timing block.

## Annex C — Open Test Suite (OTS v0.1)
- **Electrical:** ripple, hot‑plug safety for CAM/DM, ESD survivability.  
- **Functional:** boot matrix, 120 Hz panel, dual camera, suspend/resume, PD negotiation.  
- **Software:** clean dmesg (< threshold warnings), module enumeration via upx‑agent, sample Waydroid app launch.  
- **Thermal:** sustained 5 W compute < defined skin temperature envelope.

## Annex D — Illustrative Hazardous Module: UPX‑LASER (concept only)
**Why include this?** To prove UPX is *truly open* while keeping users safe. The spec must allow unusual, high‑power, or lab‑grade modules — under strict policy.
**Purpose examples** — Industrial measurement, optical alignment, research. (Not a consumer toy.)
**Safety class** — Marked **Hazardous**. Consumer devices (L≤1) **MUST NOT** enable by default. DevKits can, with owner overrides.
**Electrical & Control (conceptual)**
- Uses the **UPX‑XP expansion profile**: one high‑speed path *if needed* plus low‑speed control (I²C/SPI/UART) and a declared power budget.  
- Module must expose a **Manifest** (vendor, model, firmware version, safety class, max power, required interlocks).  
- Required signals (abstract): Enable (hardware gate; defaults OFF), Fault (module→host), Interlock (external safety switch), Temperature/Health, optional Modulation API.
**Interlocks & Enforcement**
- Backplane can **hard‑cut** power regardless of software state.  
- upx‑agent requires **owner presence**, explicit consent, and interlock OK before enable.  
- Regulatory compliance (e.g., IEC 60825) is the **module vendor’s** duty; consumer shipments must follow law.
**Takeaway** — UPX allows *anything* in principle — as long as it declares itself, respects power budgets, passes safety checks, and the **owner stays in control**.

## Annex E — UPX HAL & Manifest (sketch)
**Manifest minimal fields**
```
vendor_id, product_id, hw_rev, fw_rev,
class (CM/RFM/DM/CAM/EPM/AUX),
safety_class (Basic/Elevated/Hazardous),
power_budget (avg/peak),
interfaces (e.g., dsi:4, csi:4, pcie:x1, usb3:1, i2c:1, spi:1, gpio:N),
driver_hint (module-specific),
caps (strings),
checksum/signature (optional)
```
**HAL expectations**
- Discover module → read Manifest → bind driver(s).  
- Enforce **permissions** by class.  
- Provide a stable userspace API via `upx‑agent` (DBus/Unix socket).  
- Keep everything **OS‑agnostic**: any OS can implement the same HAL contract.
