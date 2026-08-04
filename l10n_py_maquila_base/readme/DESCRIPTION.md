Base module for Paraguay's Maquila regime (Ley 7547/2025, regulated by
Decreto 5714/2026), which replaced Ley 1064/97.

It provides the core data model shared by the rest of the maquila stack:

- **Maquila program**: biministerial resolution, legal regime (Ley 7547/2025
  or legacy Ley 1064/97), modalities (pura, servicios, capacidad ociosa,
  sub-maquila, shelter/albergue, coexistencia), foreign matrix, CNIME contract
  (OCA Agreement) and benefit duration (20 years, Art. 13).
- **Program products** with their INTN certificates and validity.
- An expiry cron that raises warning activities for programs, contracts and
  INTN certificates nearing their deadline.
