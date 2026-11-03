import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import gen_docx, gen_xlsx, gen_pptx, gen_rm
OUT = os.path.join(os.path.dirname(__file__), "..", "frontend", "files")
os.makedirs(OUT, exist_ok=True)
gen_docx.build(OUT); gen_xlsx.build(OUT); gen_pptx.build(OUT); gen_rm.build(OUT)
print("\n".join(sorted(os.listdir(OUT))))
