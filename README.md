Abre as Definições do VS Code (Ctrl + ,).Pesquisa por python.analysis.packageIndexDepths.Clica em Edit in settings.json e adiciona estas linhas dentro do objeto de configuração:json"python.analysis.packageIndexDepths": [
    {
        "name": "mlx",
        "depth": 5
    }
],
"python.analysis.extraPaths": [
    "./.venv/lib/python3.12/site-packages"
]