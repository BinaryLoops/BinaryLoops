"""Rebuild every panel, the README, then run the verification gate."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_hero, build_sections, build_projects, build_topology, build_readme, verify

if __name__ == "__main__":
    build_hero.hero()
    for fn in (build_sections.terminal, build_sections.matrix,
               build_sections.architecture, build_sections.footer):
        fn()
    for fn in (build_projects.smartchennai, build_projects.documind,
               build_projects.pocketmate, build_projects.grocery):
        fn()
    build_topology.topology()
    build_readme.build()
    print()
    verify.check()
