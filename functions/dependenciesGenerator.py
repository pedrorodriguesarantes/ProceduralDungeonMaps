import random 

class mapDependenciesGenerator:
    def __init__(self, numberPoints, maxDependencies):
        self.numberPoints = numberPoints
        self.maxDependencies = maxDependencies
        self.dependencies = list()
    
    def getDependencies(self):
        return self.dependencies 

    def generateDependencies(self):
        self.dependencies.append({
            'id': 0,
            'dependencies': [],
            'directDependencies': [],
        })

        for i in range(1, self.numberPoints):
            possibleDependenciesForPoint = self.dependencies
            numberOfPossibilities = len(possibleDependenciesForPoint)
            numberDependenciesForPoint = random.randint(1, min(numberOfPossibilities, 3))

            point = {
                'id': i,
                'dependencies': [],
                'directDependencies': []
            }

            for ii in range(0, numberDependenciesForPoint):
                if len(possibleDependenciesForPoint) == 0:
                    pass 
                
                else:
                    if len(possibleDependenciesForPoint) == 1: 
                        dependencyIndex = 0
                    else: 
                        dependencyIndex = random.randint(0, len(possibleDependenciesForPoint) - 1)

                    dependency = possibleDependenciesForPoint[dependencyIndex]
                    
                    point['dependencies'] = point['dependencies'] + dependency['dependencies'] + [dependency['id']]
                    point['directDependencies'] = point['directDependencies'] + [dependency['id']]

                    possibleDependenciesForPoint = [
                        obj for obj in possibleDependenciesForPoint 
                        if obj['id'] not in point['directDependencies']
                    ]
                    
                    possibleDependenciesForPoint = [
                        obj for obj in possibleDependenciesForPoint 
                        if obj['id'] not in point['dependencies'] and not any(dep in point['directDependencies'] for dep in obj['dependencies'])
                    ]

            if len(point['dependencies']) > 0:
                point['dependencies'] = list(set(point['dependencies']))
            
            self.dependencies.append(point)
    