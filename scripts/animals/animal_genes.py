import os
from scripts.objects.animal import AnimalBreed
from scripts.objects.animal_gene import AnimalGene
from scripts.core import constants, file_loading
from scripts.utils import echo

GENES_DIR = os.path.join(constants.ANIMAL_DIR, "genes")

def table_row(content: list[str]) -> list[str]:
    return [f"| {data}" for data in content]

def main():
    for full_breed_id, breed in AnimalBreed.all().items():
        animal = breed.animal

        # Build the genes first so we can sort before generating the table
        genes: list[AnimalGene] = []
        for gene_id in animal.genes:
            if gene_id in breed.forced_genes:
                gene = AnimalGene.from_forced_gene(gene_id, breed.forced_genes[gene_id])
            else:
                gene = AnimalGene(gene_id)

            if not gene.is_valid:
                echo.warning(f"[{breed.full_breed_id}] Gene '{gene_id}' is not valid.")
                continue
            genes.append(gene)
        
        genes.sort(key=lambda g: g.name.casefold())

        content: list[str] = []

        bot_flag_start = constants.BOT_FLAG.format(type=f"genes", id=breed.full_breed_id)
        bot_flag_end = constants.BOT_FLAG_END.format(type=f"genes", id=breed.full_breed_id)

        content.append(bot_flag_start)
        content.append('{| class="wikitable theme-red"')
        content.extend([
            "! Gene",
            "! Dominance",
            "! Value"
        ])

        has_forced_gene = False
        has_random_dominance = False
        for gene in genes:
            has_forced_gene = gene.is_forced or has_forced_gene
            has_random_dominance = gene.dominance == "Random" or has_random_dominance
            name = f"{gene.name}" + " {{Footnote|Breed|name=Breed}}" if gene.is_forced else gene.name
            dominance = "{{Footnote|Random|name=Random}}" if gene.dominance == "Random" else gene.dominance 
            value = f"{gene.min_value}–{gene.max_value}"
            content.append("|-")
            content.extend(table_row([name, dominance, value]))

        content.append("|}")
        content.append(bot_flag_end)

        if has_forced_gene:
            content.append(":{{Footnote|Breed|The value and dominance shown are specific to this breed.|name=<sup>Breed</sup>}}")
        if has_random_dominance:
            content.append(":{{Footnote|Random|Indicates that the dominance is chosen at random based on how close the value is to 0.5.|name=<sup>Random</sup>}}")

        file_loading.write_file(content, rel_path=f"{full_breed_id}.txt", root_path=GENES_DIR)

if __name__ == "__main__":
    main()
