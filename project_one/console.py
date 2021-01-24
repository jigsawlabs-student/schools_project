import project_one.src.models as models
import project_one.src.adapters as adapters
import project_one.src.db as db

school_run = adapters.ParentBuilder().school_run()
attn_run = adapters.ParentBuilder().attn_run()
pop_run = adapters.ParentBuilder().pop_run()
scores_run = adapters.ParentBuilder().scores_run()
