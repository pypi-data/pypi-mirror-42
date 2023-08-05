__version__ = '0.0.8'

# 0.0.8 - Multiple major changes
#   - Finding label errors is no fully parallelized. 
#   - prune_count_method parameter has been removed. 
#   - estimate_confident_joint_from_probabilities now automatically calibrates confident joint to be a true joint estimate.
#   - Confident joint algorithm changed! When an example is found confidently as 2+ labels, choose class with max probability.
# 0.0.7 - Massive speed increases across the board. Estimating confident joint now nearly instant. NO major API changes.
# 0.0.6 - NO API changes. README updates. Examples added. Tutorials added.
# 0.0.5 - Numerous small bug fixes, but not major API changes. 100% testing code coverage.
# 0.0.4 - FIRST CROSS-PLATFORM WORKING VERSION OF CLEANLAB. Adding test support.
# 0.0.3 - Adding working logo to README, pypi working
# 0.0.2 - Added logo to README, but link does not load on pypi
# 0.0.1 - initial commit
