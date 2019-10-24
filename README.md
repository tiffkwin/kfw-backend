# kfw-backend

> This is a toolkit for **MacOS X and Windows** that automatically analyzes data for assays.

## Understanding the Output
This section explains in detail the significance of the results of the data analysis.

### Membrane Potential
1. **Metadata Sheet** - This sheet hosts information about the experiment itself
    * ID - The experimental ID.
    * Standard Curve - A true or false value indicating whether or not the standard curve calculation was used.
    * Slope - The slope value entered by the researcher to be used in calculations.
    * Y-Intercept - The y-intercept value entered by the researcher to be used in calculations.
    * Substrates - A column containing the list of substrates used in the experiment.
    * Additions - A column containing the list of additions used in the experiment.
    * Date - The date the analysis was run in the form YYYY-MM-DD.
2. **Raw Data** - The raw data taken from the lab tools.
    * The data is in the form  X | Y | X |...
3. **Averaged Raw Data** - The average membrane potential for 3-minute (i.e., 180 seconds) increments in each data set. Each data set is annotated with the buffer conditions of the assay at that time.
4. **Corrected Raw Data** - The same data as the Average Raw Data sheet, but with an additional correction calculation which divides each average membrane potential by the the average membrane potential for Ala.
5. **Standard Curve Data** - The results of the standard curve calculation on the raw data.
    * The data is in the form  X | Y | X |...
6. **Averaged Standard Curve** - The results of the standard curve calculation on the averaged data.

### NADH Redox
1. **Metadata Sheet** - This sheet hosts information about the experiment itself.
    * ID - The experimental ID.
    * Substrates - A column containing the list of substrates used in the experiment.
    * Additions - A column containing the list of additions used in the experiment.
    * Date - The date the analysis was run in the form YYYY-MM-DD.
2. **Raw Data** - The raw data taken from the lab tools. 
    * The data is in the form  X | Y | X |...
3. **Stripped Data** - Contains only the columns that correspond to the NADH data points. 
    * The data is in the form  X | Y | X |...
4. **Reduced Data** - The same data as the Stripped Data sheet, but with an additional reduction calculation.
    * `y_new = (y_old-min)/(max-min)*100`
5. **Averaged Reduced Data** - The averages of the reduced data for 3-minute (i.e., 180 seconds) increments in each data set. Each data set is annotated with the buffer conditions of the assay at that time.

### H2O2
1. **Metadata Sheet** - This sheet hosts information about the experiment itself
    * ID - The experimental ID.
    * Standard Curve - A true or false value indicating whether or not the standard curve calculation was used.
    * Slope - The slope value entered by the researcher to be used in calculations.
    * Y-Intercept - The y-intercept value entered by the researcher to be used in calculations.
    * Substrates - A column containing the list of substrates used in the experiment.
    * Additions - A column containing the list of additions used in the experiment.
    * Mitochondria - The amount of mitochondria use (in milligrams).
    * Date - The date the analysis was run in the form YYYY-MM-DD.
2. **Raw Data** - The raw data taken from the lab tools.
    * The data is in the form  X | Y | X |...
3. **Slopes Data** - The slope for 3-minute (i.e., 180 seconds) increments in each data set. Each data set is annotated with the buffer conditions of the assay at that time.
4. **Corrected Slopes** - The same data as the Slopes sheet, but with an additional correction calculation which divides each slope value by the mg of mitochondria used.
5. **Standard Curve** - The results of the standard curve calculation on the Raw Data.
6. **Standard Curve Slopes** - The results of the standard curve calculation on the Slopes Data.
7. **Corrected Standard Curve Slopes** - The results of the correction calculation on the Standard Curve Slopes data.

### Membrane Potential Merge
Combines data from all of the Averaged Standard Curve sheets in the Membrane Potential data analysis Excel files. Each row corresponds to a substrate. The Mean and SEM is calculated for each row.

### NADH Redox Merge
Combines data from all of the Averaged Reduced Data sheets in the NADH Redox data analysis Excel files. Each row corresponds to a substrate. The Mean and SEM is calculated for each row.

### H2O2 Merge
Combines data from all of the Corrected Standard Curve Slopes sheets in the H2O2 data analysis Excel files. Each row corresponds to a substrate. The Mean and SEM is calculated for each row.

