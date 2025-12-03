echo "Collecting static files"
python3 manage.py collectstatic --noinput

echo "Building static output"
mkdir -p /vercel/output/staticfiles
cp -r staticfiles/* /vercel/output/staticfiles/
