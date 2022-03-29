import os, glob, shutil
from re import template
from pathlib import Path


os.chdir(Path('app/www/EffectPlayerClient'))
os.system('pwd')
print("##### Building Angular")
os.system('npm install')
os.system('ng build --output-hashing none --base-href /static/')
os.chdir(Path('../../..'))
os.system('pwd')
print("##### Moving files to backend")

js_files =    glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/*.js")
ico_files =   glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/*.ico")
css_files =   glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/*.css")
font_files =   glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/*.woff*")
html_files =  glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/*.html")
asset_files = glob.glob("app/www/EffectPlayerClient/dist/effect-player-client/assets/*")

static_files = js_files + ico_files + css_files + font_files
template_files = html_files

for file in static_files:
    basename = os.path.basename(file)
    print(f'  Moving to static:   {basename}')
    shutil.move(file, Path(f'app/www/static/{basename}'))

for file in asset_files:
    os.makedirs("app/www/static/assets/", exist_ok=True)
    basename = os.path.basename(file)
    print(f'  Moving to static: {basename}')
    shutil.move(file, Path(f'app/www/static/assets/{basename}'))

for file in template_files:
    basename = os.path.basename(file)
    print(f'  Moving to template: {basename}')
    shutil.move(file, Path(f'app/www/templates/{basename}'))


print("##### Build Completed")
