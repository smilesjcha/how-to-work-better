"""강의 파일만 배포 ZIP에 담는다. QA·캐시·개인 파일은 제외한다."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from fnmatch import fnmatch

ROOT = Path(__file__).resolve().parent.parent
EXCLUDES = [line.strip() for line in (ROOT/'.gitignore').read_text().splitlines()
            if line.strip() and not line.startswith('#')]


def excluded(path):
    relative = path.relative_to(ROOT).as_posix()
    return any(relative.startswith(pattern) if pattern.endswith('/') else fnmatch(relative, pattern)
               for pattern in EXCLUDES)


def files_under(folder):
    return sorted(path for path in folder.rglob('*')
                  if path.is_file() and not excluded(path) and not any(part.startswith('.') or part == '__pycache__'
                                               for part in path.relative_to(folder).parts))


def package():
    material = files_under(ROOT/'materials')
    (ROOT/'dist').mkdir(exist_ok=True)
    practice = ROOT/'dist/daeryzen-practice-kit.zip'
    complete = ROOT/'dist/daeryzen-complete-kit.zip'
    with ZipFile(practice, 'w', ZIP_DEFLATED) as z:
        for path in material:
            z.write(path, path.relative_to(ROOT/'materials'))
    complete_files = [ROOT/'README.md']+material
    for folder in ('docs', 'design'):
        complete_files.extend(files_under(ROOT/folder))
    complete_files.extend([ROOT/'output/daeryzen-ai-office-20261007.pptx',
                           ROOT/'output/daeryzen-ai-office-20261007.pdf'])
    with ZipFile(complete, 'w', ZIP_DEFLATED) as z:
        for path in complete_files:
            z.write(path, path.relative_to(ROOT))
    for path in (practice, complete):
        with ZipFile(path) as z:
            assert z.testzip() is None
            assert any('05-document-forms/wbs-gantt.csv' in name for name in z.namelist())
            assert not any('qa-' in name or '__pycache__' in name for name in z.namelist())
            assert not any(name.endswith('.inspect.ndjson') or any(private in name for private in
                           ('00-email-brief', '03-survey-design', '05-email-reply')) for name in z.namelist())
            print(f'{path.name}: {len(z.namelist())} files')


if __name__ == '__main__':
    package()
