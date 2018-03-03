//
//  CustomCell.swift
//  TableViewWithMultipleSelection
//
//  Created by Stanislav Ostrovskiy on 5/22/17.
//  Copyright © 2017 Stanislav Ostrovskiy. All rights reserved.
//

import UIKit

class ThemeCustomCell: UITableViewCell {
    
    @IBOutlet weak var titleLabel: UILabel!
    
    @IBAction func viewTheme(_ sender: Any) {
        let themeMenu = ThemesMenuViewController()
        themeMenu.performSegue(withIdentifier: "toTheme", sender: sender)
    }
    
    var item: ThemeViewModelItem? {
        didSet {
            titleLabel?.text = item?.title
        }
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        
        selectionStyle = .none
    }
    
    
    static var nib:UINib {
        return UINib(nibName: identifier, bundle: nil)
    }
    
    static var identifier: String {
        return String(describing: self)
    }
    
    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)
        
        // update UI
        accessoryType = selected ? .checkmark : .none
    }
}



