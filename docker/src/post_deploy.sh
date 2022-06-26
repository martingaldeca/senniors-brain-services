# Create pytest alias
echo 'alias pytest="python -m pytest"' >> ~/.bashrc && source ~/.bashrc

uvicorn main:app --host 0.0.0.0 --reload