//
//  TableViewCell.swift
//  Music-Driven-Workout-App
//
//  Created by techbar on 3/3/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

class TableViewCell: UITableViewCell {
        
    @IBOutlet weak var column1: UILabel!
    @IBOutlet weak var column2: UILabel!
    @IBOutlet weak var column3: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
