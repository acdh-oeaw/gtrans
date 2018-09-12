from entities.models import Institution
from . models import RepoLocation


def create_bestand(sample, split=', '):
    bestande = sample.split(split)[1:]
    inst, _ = Institution.objects.get_or_create(
        written_name=sample.split(split)[0]
    )
    repos = []
    for x in bestande:
        repo, _ = RepoLocation.objects.get_or_create(
            name=x, archiv=inst
        )
        repos.append(repo)
    counter = 1
    for x in repos[1:]:
        parent = repos[counter-1]
        child = repos[counter]
        child.part_of = parent
        child.save()
        counter += 1
    return repos
