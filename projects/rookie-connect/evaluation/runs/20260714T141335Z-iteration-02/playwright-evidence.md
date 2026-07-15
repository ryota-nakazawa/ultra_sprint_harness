# Playwright Evidence

Playwright at `http://127.0.0.1:4174` verified desktop `1440x1000` and mobile `390x844`.

| Case | Real user operation | Result |
|---|---|---|
| E-02 | Reply input hidden initially → click Reply → visible → second click → hidden | Pass |
| C-03 | Like click twice: `8 → 9 → 8`, selected state `false → true → false` | Pass |
| Mechanical gate | Captured `console.error` and `pageerror` in both viewports | Pass: none |
