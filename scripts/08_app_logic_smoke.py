"""Run app.py's *Python tab construction* with a minimal Streamlit stub.

This is not a replacement for a real Streamlit/browser run. It does execute
all tab bodies against deterministic synthetic records, catching missing
columns and Plotly figure-construction mistakes without installing Streamlit.
"""
from __future__ import annotations
import runpy, sys, types
from pathlib import Path

class Surface:
    def __enter__(self): return self
    def __exit__(self,*exc): return False
    def __getattr__(self,name):
        def call(*args,**kwargs):
            if name in ('select_slider','slider','number_input','text_input'):
                return kwargs.get('value',args[3] if name=='slider' and len(args)>3 else kwargs.get('options',[None])[0])
            if name in ('checkbox','toggle','button'):return kwargs.get('value',False)
            return None
        return call

class StreamlitStub(types.ModuleType):
    sidebar=Surface()
    def __init__(self):super().__init__('streamlit')
    def cache_data(self,*args,**kwargs):return lambda fn: fn
    def columns(self,spec,*args,**kwargs):return [Surface() for _ in range(spec if isinstance(spec,int) else len(spec))]
    def tabs(self,labels):return [Surface() for _ in labels]
    def expander(self,*args,**kwargs):return Surface()
    def radio(self,label,options,*args,**kwargs):return options[kwargs.get('index',0)]
    def selectbox(self,label,options,*args,**kwargs):return options[kwargs.get('index',0)]
    def select_slider(self,label,*args,**kwargs):return kwargs.get('value',kwargs['options'][0])
    def slider(self,label,*args,**kwargs):return kwargs.get('value',args[2] if len(args)>2 else args[0])
    def number_input(self,label,*args,**kwargs):return kwargs.get('value',0)
    def checkbox(self,label,*args,**kwargs):return kwargs.get('value',False)
    def toggle(self,label,*args,**kwargs):return kwargs.get('value',False)
    def text_input(self,label,*args,**kwargs):return kwargs.get('value','')
    def button(self,*args,**kwargs):return False
    def stop(self):raise RuntimeError('Unexpected stop in smoke test')
    def __getattr__(self,name):return lambda *args,**kwargs:None

def smoke():
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root))
    before=sys.modules.get('streamlit')
    sys.modules['streamlit']=StreamlitStub()
    try:runpy.run_path(str(root/'app.py'),run_name='__main__')
    finally:
        if before is None:sys.modules.pop('streamlit',None)
        else:sys.modules['streamlit']=before
    print('PASS: All synthetic app tabs executed with a Streamlit API stub. Not real UI verification.')
if __name__=='__main__':smoke()
