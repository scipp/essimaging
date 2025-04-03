:::{image} _static/logo.svg
:class: only-light
:alt: ESSimaging
:width: 60%
:align: center
:::
:::{image} _static/logo-dark.svg
:class: only-dark
:alt: ESSimaging
:width: 60%
:align: center
:::

```{raw} html
   <style>
    .transparent {display: none; visibility: hidden;}
    .transparent + a.headerlink {display: none; visibility: hidden;}
   </style>
```

```{role} transparent
```

# {transparent}`ESSimaging`

<span style="font-size:1.2em;font-style:italic;color:var(--pst-color-text-muted)">
  Imaging data reduction for the European Spallation Source
  </br></br>
</span>

## Imaging Data Reduction Examples
````{card}

```{button-ref} user-guide/ymir/histogram_mode_detector
:class: stretched-link

Ymir - Histogram Mode Detector

```

````

````{card}

```{button-ref} user-guide/odin/odin_simulation
:class: stretched-link

ODIN McStas Simulation - Timepix Simulation with Choppers

```

````
:::{include} user-guide/installation.md
:heading-offset: 1
:::

## Get in touch

- If you have questions that are not answered by these documentation pages, ask on [discussions](https://github.com/scipp/essimaging/discussions). Please include a self-contained reproducible example if possible.
- Report bugs (including unclear, missing, or wrong documentation!), suggest features or view the source code [on GitHub](https://github.com/scipp/essimaging).

```{toctree}
---
hidden:
---

user-guide/index
api-reference/index
developer/index
about/index
```
