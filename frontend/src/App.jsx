import { useState } from "react";

const API = "";

export default function App() {
  const [view, setView] = useState("home");
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState(null);
  const [homeValue, setHomeValue] = useState("");
  const [over65, setOver65] = useState(false);
  const [taxResult, setTaxResult] = useState(null);
  const [taxLoading, setTaxLoading] = useState(false);
  const [filter, setFilter] = useState("all");

  async function handleSearch(e) {
    e.preventDefault();
    if (!address.trim()) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(
        `${API}/api/lookup?address=${encodeURIComponent(address)}`,
      );
      const data = await res.json();
      setResults(data);
      setView(data.covered ? "results" : "notcovered");
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleTax(e) {
    e.preventDefault();
    if (!homeValue) return;
    setTaxLoading(true);
    try {
      const res = await fetch(`${API}/api/tax-impact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          home_value: parseFloat(homeValue),
          over_65: over65,
        }),
      });
      const data = await res.json();
      setTaxResult(data);
    } catch {
      setTaxResult(null);
    } finally {
      setTaxLoading(false);
    }
  }

  const categories = [
    "all",
    "budget",
    "contract",
    "zoning",
    "school_policy",
    "tax_rate",
    "personnel",
    "other",
  ];

  const filteredItems =
    results?.items?.filter(
      (item) => filter === "all" || item.category === filter,
    ) ?? [];

  const exampleAddresses = ["16327 Lakeview Dr, Jersey Village TX 77040"];

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <div className="logo">LocalLens</div>
          <div className="tagline">Local government, made simple.</div>
        </div>
      </header>

      {view === "home" && (
        <main className="main">
          <section className="hero">
            <h1 className="hero-title">
              What's being decided
              <br />
              in your community?
            </h1>
            <p className="hero-sub">
              Enter your address to see city council and school board decisions
              that affect you, explained in plain English.
            </p>
            <form className="search-form" onSubmit={handleSearch}>
              <input
                className="search-input"
                type="text"
                placeholder="e.g. 16327 Lakeview Dr, Jersey Village TX"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                disabled={loading}
              />
              <button className="search-btn" type="submit" disabled={loading}>
                {loading ? "Searching..." : "Search"}
              </button>
            </form>
            {error && <p className="error-msg">{error}</p>}
            <p className="coverage-note">
              Currently covers <strong>Jersey Village</strong> and{" "}
              <strong>Cypress-Fairbanks ISD</strong>.
            </p>
          </section>

          <section className="how-it-works">
            <h2 className="section-title">How it works</h2>
            <div className="steps">
              <div className="step">
                <div className="step-num">1</div>
                <div>
                  <div className="step-head">Enter your address</div>
                  <div className="step-body">
                    We figure out which city council and school board represent
                    you.
                  </div>
                </div>
              </div>
              <div className="step">
                <div className="step-num">2</div>
                <div>
                  <div className="step-head">See what is on the agenda</div>
                  <div className="step-body">
                    Recent and upcoming decisions, explained in plain English.
                  </div>
                </div>
              </div>
              <div className="step">
                <div className="step-num">3</div>
                <div>
                  <div className="step-head">Know what it costs you</div>
                  <div className="step-body">
                    See the real dollar impact of tax votes on your household.
                  </div>
                </div>
              </div>
            </div>
          </section>
        </main>
      )}

      {view === "notcovered" && (
        <main className="main">
          <div className="not-covered">
            <h2 className="nc-title">We do not cover that area yet</h2>
            <p className="nc-body">
              LocalLens currently covers <strong>Jersey Village</strong> and{" "}
              <strong>Cypress-Fairbanks ISD</strong>. We are working on
              expanding to more communities.
            </p>
            <p className="nc-body">Try one of these addresses to see a demo:</p>
            <div className="example-addresses">
              {exampleAddresses.map((addr) => (
                <button
                  key={addr}
                  className="example-btn"
                  onClick={() => {
                    setAddress(addr);
                    setView("home");
                  }}
                >
                  {addr}
                </button>
              ))}
            </div>
            <button
              className="back-btn"
              onClick={() => {
                setView("home");
                setAddress("");
              }}
            >
              Search a different address
            </button>
          </div>
        </main>
      )}

      {view === "results" && results && (
        <main className="main">
          <div className="results-header">
            <div className="results-address">
              Results for <span className="address-text">{address}</span>
            </div>
            <button
              className="change-btn"
              onClick={() => {
                setView("home");
                setResults(null);
                setTaxResult(null);
              }}
            >
              Change address
            </button>
          </div>

          <div className="coverage-tags">
            {results.city && (
              <span className="tag tag-city">{results.city}</span>
            )}
            {results.isd && <span className="tag tag-isd">{results.isd}</span>}
          </div>

          <section className="feed-section">
            <div className="feed-header">
              <h2 className="section-title">Agenda items</h2>
              <div className="filter-row">
                {categories.map((cat) => (
                  <button
                    key={cat}
                    className={`filter-btn ${filter === cat ? "active" : ""}`}
                    onClick={() => setFilter(cat)}
                  >
                    {cat === "all" ? "All" : cat.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>

            {filteredItems.length === 0 ? (
              <p className="empty-msg">No items found for this filter.</p>
            ) : (
              <div className="feed">
                {filteredItems.map((item) => (
                  <div className="item" key={item.id}>
                    <div className="item-meta">
                      <span className={`item-cat cat-${item.category}`}>
                        {item.category?.replace("_", " ")}
                      </span>
                      {item.action_required && (
                        <span className="item-vote">Vote</span>
                      )}
                      <span className="item-date">
                        {item.meeting_date?.replace(".pdf", "") || ""}
                      </span>
                    </div>
                    <p className="item-summary">{item.plain_summary}</p>
                    {item.amounts &&
                      JSON.parse(item.amounts || "[]").length > 0 && (
                        <div className="item-amounts">
                          {JSON.parse(item.amounts).map((amt, i) => (
                            <span key={i} className="amount-tag">
                              {amt}
                            </span>
                          ))}
                        </div>
                      )}
                    {item.verified && (
                      <div className="item-verified">
                        Verified against source
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="tax-section">
            <h2 className="section-title">What does this cost you?</h2>
            <p className="tax-intro">
              Estimate the impact of CFISD's latest tax rate change on your
              household. School tax only, does not include city, county, or
              other taxing units.
            </p>
            <form className="tax-form" onSubmit={handleTax}>
              <div className="tax-row">
                <label className="tax-label">
                  Home appraised value
                  <input
                    className="tax-input"
                    type="number"
                    placeholder="e.g. 300000"
                    value={homeValue}
                    onChange={(e) => setHomeValue(e.target.value)}
                  />
                </label>
                <label className="tax-check-label">
                  <input
                    type="checkbox"
                    checked={over65}
                    onChange={(e) => setOver65(e.target.checked)}
                  />
                  Over 65 or disabled
                </label>
              </div>
              <button className="tax-btn" type="submit" disabled={taxLoading}>
                {taxLoading ? "Calculating..." : "Calculate my bill"}
              </button>
            </form>

            {taxResult && (
              <div className="tax-result">
                <div className="tax-grid">
                  <div className="tax-cell">
                    <div className="tax-cell-label">Taxable value</div>
                    <div className="tax-cell-value">
                      ${taxResult.taxable_value.toLocaleString()}
                    </div>
                  </div>
                  <div className="tax-cell">
                    <div className="tax-cell-label">2024 bill</div>
                    <div className="tax-cell-value">
                      ${taxResult.current_bill.toLocaleString()}
                    </div>
                  </div>
                  <div className="tax-cell">
                    <div className="tax-cell-label">2025 bill</div>
                    <div className="tax-cell-value">
                      ${taxResult.proposed_bill.toLocaleString()}
                    </div>
                  </div>
                  <div className="tax-cell">
                    <div className="tax-cell-label">Difference</div>
                    <div
                      className={`tax-cell-value ${taxResult.difference < 0 ? "positive" : "negative"}`}
                    >
                      {taxResult.difference < 0 ? "-" : "+"}$
                      {Math.abs(taxResult.difference).toLocaleString()} / year
                    </div>
                  </div>
                </div>
                <p className="tax-note">{taxResult.note}</p>
              </div>
            )}
          </section>
        </main>
      )}

      <footer className="footer">
        <div className="footer-inner">
          <p>
            LocalLens covers Jersey Village city council and Cypress-Fairbanks
            ISD. Summaries are verified against source documents and are for
            informational purposes only.
          </p>
          <p className="footer-built">
            Built for the 2026 Congressional App Challenge.
          </p>
        </div>
      </footer>
    </div>
  );
}
