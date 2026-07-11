from collections import Counter


class StatisticsService:

    def build(self, connections):

        countries = Counter()
        publishers = Counter()
        processes = Counter()

        for c in connections:

            countries[c.country_name] += 1
            publishers[c.publisher] += 1
            processes[c.process] += 1

        return {

            "countries": countries,

            "publishers": publishers,

            "processes": processes,

            "total": len(connections),

        }