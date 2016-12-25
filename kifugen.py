#!/usr/bin/python3
import argparse

import sgftools.diagramgenerators
import sgftools.parser
import sgftools.problemspdfbuilder


def generate_problems(args):
    sgf_parser = sgftools.parser.SgfParser()
    game = sgf_parser.load_game(args.input)

    generator = sgftools.diagramgenerators.ProblemsBookGenerator()
    tasks = generator.generate(game, title="Problem")

    generator = sgftools.problemspdfbuilder.ProblemsPdfBuilder(trim_board=args.trim_board)
    generator.add_diagrams(tasks)
    generator.save(args.output)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

problems_parser = subparsers.add_parser('problems')
problems_parser.add_argument('-i', "--input", required=True)
problems_parser.add_argument('-o', '--output', required=True)
problems_parser.add_argument('--trim-board', help="cut diagrams in problems")
problems_parser.set_defaults(func=generate_problems)


if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)


