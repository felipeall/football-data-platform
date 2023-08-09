from dataclasses import dataclass

from sqlalchemy import Column, Float, Integer, String, UniqueConstraint

from app.models.base import AuditMixin, Base, IDMixin


@dataclass
class FBRefMatchesReports(Base, IDMixin, AuditMixin):
    __tablename__ = "matches_reports"
    __table_args__ = (
        UniqueConstraint("match_id", "team_id", "player_id"),
        {"schema": "fbref"},
    )

    match_id: str = Column(String, nullable=False)
    team_id: str = Column(String, nullable=False)
    player_id: str = Column(String, nullable=False)
    player_name: str = Column(String, nullable=False)
    min: int = Column(Integer, nullable=False)
    performance_gls: int = Column(Integer, nullable=True)
    performance_ast: int = Column(Integer, nullable=True)
    performance_pk: int = Column(Integer, nullable=True)
    performance_pkatt: int = Column(Integer, nullable=True)
    performance_sh: int = Column(Integer, nullable=True)
    performance_sot: int = Column(Integer, nullable=True)
    performance_touches: int = Column(Integer, nullable=True)
    performance_tkl: int = Column(Integer, nullable=True)
    performance_blocks: int = Column(Integer, nullable=True)
    expected_xg: float = Column(Float, nullable=True)
    expected_npxg: float = Column(Float, nullable=True)
    expected_xag: float = Column(Float, nullable=True)
    sca_sca: int = Column(Integer, nullable=True)
    sca_gca: int = Column(Integer, nullable=True)
    passes_cmp: int = Column(Integer, nullable=True)
    passes_att: int = Column(Integer, nullable=True)
    passes_cmp_pct: float = Column(Float, nullable=True)
    passes_prgp: int = Column(Integer, nullable=True)
    total_cmp: int = Column(Integer, nullable=True)
    total_att: int = Column(Integer, nullable=True)
    total_cmp_pct: float = Column(Float, nullable=True)
    total_totdist: int = Column(Integer, nullable=True)
    total_prgdist: int = Column(Integer, nullable=True)
    short_cmp: int = Column(Integer, nullable=True)
    short_att: int = Column(Integer, nullable=True)
    short_cmp_pct: float = Column(Float, nullable=True)
    medium_cmp: int = Column(Integer, nullable=True)
    medium_att: int = Column(Integer, nullable=True)
    medium_cmp_pct: float = Column(Float, nullable=True)
    long_cmp: int = Column(Integer, nullable=True)
    long_att: int = Column(Integer, nullable=True)
    long_cmp_pct: float = Column(Float, nullable=True)
    ast: int = Column(Integer, nullable=True)
    xag: float = Column(Float, nullable=True)
    xa: float = Column(Float, nullable=True)
    kp: int = Column(Integer, nullable=True)
    final_third: int = Column(Integer, nullable=True)
    ppa: int = Column(Integer, nullable=True)
    crspa: int = Column(Integer, nullable=True)
    prgp: int = Column(Integer, nullable=True)
    att: int = Column(Integer, nullable=True)
    pass_types_live: int = Column(Integer, nullable=True)
    pass_types_dead: int = Column(Integer, nullable=True)
    pass_types_fk: int = Column(Integer, nullable=True)
    pass_types_tb: int = Column(Integer, nullable=True)
    pass_types_sw: int = Column(Integer, nullable=True)
    pass_types_crs: int = Column(Integer, nullable=True)
    pass_types_ti: int = Column(Integer, nullable=True)
    pass_types_ck: int = Column(Integer, nullable=True)
    corner_kicks_in: int = Column(Integer, nullable=True)
    corner_kicks_out: int = Column(Integer, nullable=True)
    corner_kicks_str: int = Column(Integer, nullable=True)
    outcomes_cmp: int = Column(Integer, nullable=True)
    outcomes_off: int = Column(Integer, nullable=True)
    outcomes_blocks: int = Column(Integer, nullable=True)
    tackles_tkl: int = Column(Integer, nullable=True)
    tackles_tklw: int = Column(Integer, nullable=True)
    tackles_def_3rd: int = Column(Integer, nullable=True)
    tackles_mid_3rd: int = Column(Integer, nullable=True)
    tackles_att_3rd: int = Column(Integer, nullable=True)
    challenges_tkl: int = Column(Integer, nullable=True)
    challenges_att: int = Column(Integer, nullable=True)
    challenges_tkl_pct: float = Column(Float, nullable=True)
    challenges_lost: int = Column(Integer, nullable=True)
    blocks_blocks: int = Column(Integer, nullable=True)
    blocks_sh: int = Column(Integer, nullable=True)
    blocks_pass: int = Column(Integer, nullable=True)
    intercep: int = Column(Integer, nullable=True)
    tkl_plus_intercep: int = Column(Integer, nullable=True)
    clr: int = Column(Integer, nullable=True)
    err: int = Column(Integer, nullable=True)
    touches_touches: int = Column(Integer, nullable=True)
    touches_def_pen: int = Column(Integer, nullable=True)
    touches_def_3rd: int = Column(Integer, nullable=True)
    touches_mid_3rd: int = Column(Integer, nullable=True)
    touches_att_3rd: int = Column(Integer, nullable=True)
    touches_att_pen: int = Column(Integer, nullable=True)
    touches_live: int = Column(Integer, nullable=True)
    take_ons_att: int = Column(Integer, nullable=True)
    take_ons_succ: int = Column(Integer, nullable=True)
    take_ons_succ_pct: float = Column(Float, nullable=True)
    take_ons_tkld: int = Column(Integer, nullable=True)
    take_ons_tkld_pct: float = Column(Float, nullable=True)
    carries_carries: int = Column(Integer, nullable=True)
    carries_totdist: int = Column(Integer, nullable=True)
    carries_prgdist: int = Column(Integer, nullable=True)
    carries_prgc: int = Column(Integer, nullable=True)
    carries_final_third: int = Column(Integer, nullable=True)
    carries_cpa: int = Column(Integer, nullable=True)
    carries_mis: int = Column(Integer, nullable=True)
    carries_dis: int = Column(Integer, nullable=True)
    receiving_rec: int = Column(Integer, nullable=True)
    receiving_prgr: int = Column(Integer, nullable=True)
    performance_crdy: int = Column(Integer, nullable=True)
    performance_crdr: int = Column(Integer, nullable=True)
    performance_2crdy: int = Column(Integer, nullable=True)
    performance_fls: int = Column(Integer, nullable=True)
    performance_fld: int = Column(Integer, nullable=True)
    performance_off: int = Column(Integer, nullable=True)
    performance_crs: int = Column(Integer, nullable=True)
    performance_intercep: int = Column(Integer, nullable=True)
    performance_tklw: int = Column(Integer, nullable=True)
    performance_pkwon: int = Column(Integer, nullable=True)
    performance_pkcon: int = Column(Integer, nullable=True)
    performance_og: int = Column(Integer, nullable=True)
    performance_recov: int = Column(Integer, nullable=True)
    aerial_duels_won: int = Column(Integer, nullable=True)
    aerial_duels_lost: int = Column(Integer, nullable=True)
    aerial_duels_won_pct: float = Column(Float, nullable=True)
