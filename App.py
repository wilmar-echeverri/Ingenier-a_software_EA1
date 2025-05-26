streamlit.errors.StreamlitDuplicateElementKey: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).

Traceback:
File "/mount/src/ingenier-a_software_ea2/App.py", line 181, in <module>
    mostrar_tabla(registros)
    ~~~~~~~~~~~~~^^^^^^^^^^^
File "/mount/src/ingenier-a_software_ea2/App.py", line 163, in mostrar_tabla
    if col7.button("Registrar salida", key=f"salida_{reg['id']}"):
       ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/runtime/metrics_util.py", line 444, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/button.py", line 243, in button
    return self.dg._button(
           ~~~~~~~~~~~~~~~^
        label,
        ^^^^^^
    ...<10 lines>...
        ctx=ctx,
        ^^^^^^^^
    )
    ^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/widgets/button.py", line 1007, in _button
    element_id = compute_and_register_element_id(
        "button",
    ...<8 lines>...
        use_container_width=use_container_width,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/utils.py", line 239, in compute_and_register_element_id
    _register_element_id(ctx, element_type, element_id)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/streamlit/elements/lib/utils.py", line 140, in _register_element_id
    raise StreamlitDuplicateElementKey(user_key)
