"""Contains the DrillSolverSettings class
"""

import os
from . import TMPLT_ENV
from .utilities import read_TO_file
from ..adripy import get_cdb_location, get_cdb_path, get_full_path

class DrillSolverSettings():
    """Creates an object with all data necessary to write an Adams Drill solver settings (.ssf) file. 
    
    Attributes
    ----------
    name : str
        Name of the solver settings object
    parameters : dict
        Dictionary of parameters that make up an Adams Drill solver settings and would be found in an Adams Drill solver settings file (.ssf).  The keys of the dictionary are the parameter names that would be seen in the string file and the values of the dictionary are the values that would be seen in the string file.
    filename : str
        Name of the solver settings file (.ssf) in which these solver settings are stored.  This attribute is initially empty and is populated by the `write_to_file()` method.
    SCALAR_PARAMETERS : list
        A class attribute listing the names of all scalar parameters found in an Adams Drill solver settings file.
    DEFAULT_PARAMETER_SCALARS : dict
        A class attribute defining defaults for some of the string parameters.
    ARRAY_PARAMETERS : list 
        A class attribute listing the names of all array parameters found in an Adams Drill solver settings file.
    DEFAULT_PARAMETER_ARRAYS : dict
        A class attribute defining defaults for some of the string parameters.
    CDB_TABLE : str
        A class attribute defining the cdb table to be used for Adams Drill solver settings files (.ssf)
    EXT : str
        A class attribute defining the extension of the Adams Drill string files.
    """
    

    SCALAR_PARAMETERS = [
        'Integrator',
        'Formulation',
        'Corrector',
        'Error',
        'HMax',
        'Alpha',
        'Thread_Count'
    ]
    DEFAULT_PARAMETER_SCALARS = {
        'Integrator': 'HHT',
        'Formulation': 'I3',
        'Corrector': 'Modified',
        'Error': 0.00001,
        'HMax': 0.005,
        'Alpha': -0.25,
        'Thread_Count': 4
    }

    ARRAY_PARAMETERS = [
        'Funnel'
    ]

    DEFAULT_PARAMETER_ARRAYS = {
        'Funnel': [
            [500, 500, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 100],
            [0.1, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [0.1, 1, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.01, 0.01, 0.005, 0.005, 0.005, 0.005],
            [0.1, 1, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05, 0.05, 0.01, 0.01, 0.005, 0.005, 0.001, 0.0005, 0.005],
            [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    }

    CDB_TABLE = 'solver_settings.tbl'
    EXT = 'ssf'
    
    def __init__(self, name, **kwargs):
        self.name = name
        self.parameters = kwargs
        
        # Apply default parameters from Class Variable
        self._apply_defaults()
        
        # Initialize filename instance variable
        self.filename = ''

    def write_to_file(self, filename, directory=None, cdb=None):
        """Creates a solver settings file from the DrillSolverSettings object.
        
        Keyword Arguments:
            write_directory {string} -- (OPTIONAL) Directory in which to write the file. Defaults to current working directory.
            filename {string} -- (OPTIONAL) Name of the file to write.  Defaults to self.name
            cdb {string} -- (OPTIONAL) Name of the cdb in which to write the file.  This argument overrides the write_directory.
        
        Raises:
            ValueError -- Raised if not all parameters have been defined.
        """
        # Raise an error if the parameters can't be validated
        if not self.validate():
            raise ValueError('The parameters could not be validated.')
        
        if directory is not None:
            # If the write_directory argument is passed, strip the filename of
            # it's path and extension
            filename = os.path.split(filename)[-1].replace(f'.{self.EXT}','')
            
            # Set the filepath to the filename in the given directory
            filepath = os.path.join(directory, filename + f'.{self.EXT}')

        elif cdb is not None:
            # If the write_directory argument is not passed, but the cdb
            # argument is, strip the filename of it's path and extension
            filename = os.path.split(filename)[-1].replace(f'.{self.EXT}','')
            
            # Set the filepath to the file in the cdb
            filepath = get_full_path(os.path.join(cdb, self.CDB_TABLE, filename + f'.{self.EXT}'))

        elif filename is not None:
            # If Nothing but a filename is given, set that as the full path
            filepath = os.path.normpath(filename.replace(f'.{self.EXT}',''))            

        else:
            # If nothing is given, raise an error
            raise ValueError('One of the following must key work arguments must be defined: write_directory, filename, cdb')
                      
        # Get the jinja2 template for a solver settings file
        ssf_template = TMPLT_ENV.get_template(f'template.{self.EXT}')

        # Write the solver settings file
        with open(filepath, 'w') as fid:
            fid.write(ssf_template.render(self.parameters))

        # Update the instance's filename attribute
        self.filename = get_cdb_path(filepath)

        # Return the name of the file that was written
        return self.filename


    def validate(self):
        """
        Determines if all parameters have been set
        
        Returns:
            Bool -- True if all parameters have been set. Otherwise False
        """
        validated = True        
        # Check that all parameters exist in the self.parameters dictionary
        for param_name in self.SCALAR_PARAMETERS:
            if param_name not in self.parameters:
                validated = False        
        
        for param_name in self.ARRAY_PARAMETERS:
            if not self.parameters[param_name]:
                validated = False
            
        return validated     
    
    @classmethod
    def read_from_file(cls, filename):
        """Reads a string file and returns a DrillString object
        with DrillString.parameters based on data in the string 
        file.
        
        Arguments:
            filename {str} -- Filename of a .str file.
            
        Returns:
            {DrillSolverSettings} -- DrillString object with 
                                     parameters from the passed 
                                     string file.
        """
        # Read the TO data into a dictionary
        tiem_orbit_data = read_TO_file(get_full_path(filename))

        drill_solver_settings = cls('')
        
        # Extract the DrillString parameters from the TO dictionary        
        drill_solver_settings._get_params_from_TO_data(tiem_orbit_data) #pylint: disable=protected-access

        return drill_solver_settings

    def _apply_defaults(self):
        """
        Applies defaults from class variables
        """
        # Applies normal parameter defaults
        for scalar_parameter, value in self.DEFAULT_PARAMETER_SCALARS.items():
            if scalar_parameter not in self.parameters:
                self.parameters[scalar_parameter] = value

        # Applies defaults to all ramp parameters
        for array_parameter, array in self.DEFAULT_PARAMETER_ARRAYS.items():
            self.parameters[array_parameter] = {}
            self.parameters[array_parameter] = array
            self.parameters['_' + array_parameter] = zip(*self.parameters[array_parameter])

    
    def _get_params_from_TO_data(self, tiem_orbit_data): #pylint: disable=invalid-name
        """Reads the solver settings parameters out of a 
        dictoinary of Tiem Orbit data generated by 
        adripy.utilities.read_TO_file()
        
        Arguments:
            tiem_orbit_data {dict} -- Dictionary of Tiem Orbit 
                                      data
        
        Raises:
            ValueError -- A solver settings parameter could not 
                          be found
        """

        for param in self.ARRAY_PARAMETERS:
            # For each string parameter initialize a found flag
            found = False
            
            if param.lower() == 'funnel':
                for i, par in enumerate(['maxit', 'stability', 'error', 'imbalance', 'tlimit', 'alimit']):
                    self.parameters[param][i] = tiem_orbit_data['STATICS']['FUNNEL'][par]
                self.parameters['_' + param] = zip(*self.parameters[param])
                found = True
            
            # Raise a value error if the parameter isn't found.
            if not found:
                raise ValueError(f'{param} not found!')

        for param in self.SCALAR_PARAMETERS:
            # For each string parameter initialize a found flag
            found = False

            for block in tiem_orbit_data:
                # For each block in the TO file

                if block !='STATICS' and param.lower() in tiem_orbit_data[block]:
                    # If the parameter is in this block, set the parameter and break the loop
                    self.parameters[param] = tiem_orbit_data[block][param.lower()]
                    found = True
                    break
 
                elif block != 'STATICS':
                    # If the parameter is not in this block, find all the sub blocks 
                    # and look for the parameter inside each sub block
                    sub_blocks = [header for header in tiem_orbit_data[block] if isinstance(tiem_orbit_data[block][header], dict)]
                    
                    for sub_block in sub_blocks:
                        # For each sub_block in the block

                        if param.lower() in [p.lower() for p in tiem_orbit_data[block][sub_block]]:
                            # If the parameter is in the sub block, set the parameter and break the loop
                            self.parameters[param] = tiem_orbit_data[block][sub_block][param.lower()]
                            found = True
                            break
                    
                    if found:
                        break
            
            # Raise a value error if the parameter isn't found.
            if not found:
                raise ValueError(f'{param} not found!')
