{% include list.liquid all=true %}

Runners are the machines that execute jobs in a GitHub Actions workflow. You can access [Variables](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables) and [Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context) information in [specific OS](https://stackoverflow.com/a/57948488/4058484). For example, a runner can clone your repository locally, install testing software, and then run commands.

```
{% raw %}
# Sample workflow for building and deploying a Jekyll site to GitHub Pages
name: Build and deploy Jekyll site

# 💎 Runs on deployment targeting the default branch
on:
  # push:
    # branches: [eQ19]
  workflow_run:
    types: [completed] #requested
    workflows: ["pages-build-deployment"]

# 🪂 Allow only one concurrent deployment across the branches
concurrency:
  group: "pages"
  cancel-in-progress: true
  
# Sets permissions of the GITHUB_TOKEN
permissions: write-all

# Sets global environtment variables
env:
  OWNER: ${{ github.repository_owner }}

jobs:
  # Build job
  github-pages:
    if: github.event.workflow_run.conclusion == 'success'
    runs-on: ${{ vars.OWNER != 'FeedMapping' && 'ubuntu-latest' || 'windows-latest' }}
    steps:
      - name: 📂 Checkout
        uses: actions/checkout@v3
        with:
          submodules: recursive
 
      - name: 💎 Build on Linux
        if: runner.os == 'Linux'
        uses: eq19/feed@v2
        with:
          pre_build_commands: 'make build'
          token: ${{ secrets.JEKYLL_GITHUB_TOKEN }}

      - name: 💎 Build on Windows
        if: runner.os == 'Windows'
        uses: eq19/maps@v1
        id: stepid
        with:
          dotnet-version: '3.1.x'
{% endraw %}
```

By deploying containers on Compute Engine, you can simplify app deployment while controlling four dimensional space. You can configure a virtual machine (VM) instance or an instance template to deploy and launch a Docker container.

![default](https://user-images.githubusercontent.com/8466209/245677838-a0fb916e-c1f2-468f-a73d-2d6acdefa529.png)

This property would tend the ballancing scheme of MEC30 so it will let 30-18=12 pairing with another 12 of 24 spins prime hexagon. The 24 goes to the center of _[True Prime Pairs](https://www.eq19.com/addition/file02.html#true-prime-pairs)_ ny the prime pair 13 and 11 and let the crancks of 2,3,5,7 inside the 10 ranks.

```
                                | 
                                |                              ----------- 5 -----------
                                |                             |                         |  
                                ↓                             ↑                         ↓
 |   feeding    |     mapping     |  lexering    |  parsering   |   syntaxing   |  grammaring  |
 |------------- 36' --------------|----------------------------36' ----------------------------|
 |     19'      |        17'      |      13'     |      11'     |       7'      |       5'     |
 +----+----+----+---+----+----+---+---+----+-----+----+----+----+----+----+-----+----+----+----+
 |  1 |  2 |  3 | 4 |  5 |  6 | 7 | 8 |  9 |  10 | 11 | 12 | 13 | 14 | 15 |  16 | 17 | 18 | 19 |
 +----+----+----+---+----+----+---+---+----+-----+----+----+----+----+----+-----+----+----+----+
 |  2 | 60 | 40 | 1 | 30 | 30 | 5 | 1 | 30 | 200 |  8 | 40 | 50 |  1 | 30 | 200 |  8 | 10 | 40 |
 +----+----+----+---+----+----+---+---+----+-----+----+----+----+----+----+-----+----+----+----+
                                ↓                             ↑                         |    |
                                |                             |                         |    |
                                 ------------ 10 -------------                          |    |
                                                                                        ↓    ↓ |
                                                                                +----+----+----+
                                                                                |  2 | 60 | 40 |
                                                                                +----+----+----+
                                                                                        |    | |
                                                                                     2+100 ◄- 
   -----------------------+----+----+----+----+----+----+----+----+----+-----           |
   True Prime Pairs Δ    |  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | Sum             |
  =======================+====+====+====+====+====+====+====+====+====+=====            ↓
   19 → π(10)            |  2 |  3 |  5 |  7 |  - |  - |  - |  - |  - | 4th  ◄- 4 =  π(10)
  -----------------------+----+----+----+----+----+----+----+----+----+-----
```

This 71 is a conformation that it has the same result as we have explained on the residual objects of 571 turn to a vektor of 71 while the rest of 500 turn to 200 objects of 3's identity and the last objects of 300 goes to the next cycles.

![default](https://user-images.githubusercontent.com/36441664/105903095-0e64bd80-6052-11eb-83ed-10190be497c5.png)

So now out of 1000 numbers that generated from 1000 primes we will get the rest of 1000 - 100 = 900. This 900 will behave as **matrix square 30x30** and act as [the base frame](https://gist.github.com/eq19/0ce5848f7ad62dc46dedfaa430069857#true-prime-pairs) of 2nd and 3rd layer which are working on π(π(100x100))-1=200 primes:

```liquid
                            33+34=67=19th prime
 |----------------------------------|-------------------------------------------------------------|
 |             33                   |                             34                              |
 |--------------|-------------------|------------------------------|------------------------------|
 |     lexering = π(1000)           |                    parsering = 1000/Φ                       |
 |--------------|-------------------|------------------------------|------------------------------|
 |   feeding    |      mapping      |          syntaxing           |          grammaring          |
 +----+----+----+----+----+----+----+----+----+-----+----+----+----+----+----+-----+----+----+----+
 | 30 | 31 | 32 | 33 | 34 | 35 | 36 | 37 | 38 |  39 | 40 | 41 | 42 | 43 | 44 | 45  | 46 | 47 | 48 |
 +----+----+----+----+----+----+----+----+----+-----+----+----+----+----+----+-----+----+----+----+
 |  2 | 60 | 40 | 1  | 30 | 30 | 5  | 1  | 30 | 200 |  8 | 40 | 50 |  1 | 30 | 200 |  8 | 10 | 40 |
 +----+----+----+----+----+----+----+----+----+-----+----+----+----+----+----+-----+----+----+----+
 |       2'     |        3'         |              5'              |               7'             | 
```

![](https://user-images.githubusercontent.com/8466209/222020262-cffc624a-b92c-4137-b76a-5423df7fc5ad.png)

![default](https://user-images.githubusercontent.com/8466209/205431468-6777265f-63a8-42ea-b454-d45227478362.png)

![](https://user-images.githubusercontent.com/8466209/236091657-62397dbe-fb87-46a2-8676-f4903b6efd3f.png)

The GitHub hosted runner is assigned to run the Linux container and a Windows Server Core container simultaneously. This is an experimental feature of Microsoft WSL2 and may have some issues. One known problem is volumes are not stable.

![Set WSL](https://user-images.githubusercontent.com/8466209/226080396-235a1645-8a58-49c4-9754-8bac362a72fa.png)

The 10 ranks will coordinate with the 18 to raise up the symmetrical behaviour of 12+24=36 which is prime pair 17+19=36 and let the 2 and 3 out of 2,3,5,7 to begin a new cycle while the 5,7 will pair the 11,13 and 17,19 as _[True Prime Pairs](https://www.eq19.com/addition/file02.html#true-prime-pairs)_.

[![default](https://user-images.githubusercontent.com/8466209/244139208-378b2229-c3e8-4f1f-8829-dee6687348fb.png)](https://commons.wikimedia.org/wiki/File:RiemannZeta_Zeros.svg)

![default](https://user-images.githubusercontent.com/8466209/202854712-3a6ef332-ae62-4af2-87d2-c8e4b1dd1c37.png)
