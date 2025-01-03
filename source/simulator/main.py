import source.simulator.LChars.main as mainLChars
import source.simulator.LPaths.main as mainLPaths


def main():
    """
    main method to call data generation of learner characteristics
    and learning paths
    """
    mainLPaths.main()
    mainLChars.main()


if __name__ == "__main__":
    main()
