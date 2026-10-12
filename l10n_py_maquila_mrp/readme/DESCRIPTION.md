Manufacturing (MRP) integration for Paraguay's Maquila regime (Ley 7547/2025):

- **BOM INTN coefficients**: gross quantity (requirement factor), net quantity
  and loss percentage, plus the origin type of each component (temporary
  admission, national, Mercosur, imported). The net-quantity fields are derived
  from GRAP's `mrp_bom_line_net_qty`.
- **Maquila program** on manufacturing orders (computed from the BOM) with BOM,
  production and waste counters.
- **Waste management** (scrap, byproduct, defective) with destruction /
  nationalization / re-export destinations; destruction drafts a stock scrap.
- **VAN wizard**: national added value for a period, computed from the program's
  analytic cost minus foreign-origin inputs; it requires completed production
  to determine the origin split.

Known gap (Phase 2): Ley 7547/2025 Art. 37 defines the national added value as
the sum of (a) goods acquired in the national territory, (b) services hired in
the country, (c) salaries and social security paid in the country, (d)
depreciation of the capital goods owned by the maquiladora and (e) the
remuneration received for the maquila or sub-maquila services. The VAN wizard
does not compute these five components: it takes the cost booked to the
program's analytic account and subtracts the inputs of imported and Mercosur
origin. It is only as complete as the analytic bookings (depreciation and the
remuneration of the maquila service, items (d) and (e), are not identified) and
must be checked against the Art. 37 components before filing the sworn
statement.
