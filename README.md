### Solar-collector-lowcost

Selects data from the following table:

| measurements_detailed |
|-----------------------|
| id                    |
| time                  |
| label                 |
| count                 |
| min                   |
| max                   |
| mean                  |
| stdev                 |

Need 1 query for each quantity:

```SELECT time, mean FROM measurements_detailed WHERE label=%s```