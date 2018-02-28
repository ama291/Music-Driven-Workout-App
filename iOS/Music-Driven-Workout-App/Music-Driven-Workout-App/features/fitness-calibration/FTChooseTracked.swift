//
//  FTChooseTracked.swift
//  Music-Driven-Workout-App
//
//  Created by Lucy Newman on 2/28/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import UIKit

private let reuseIdentifier = "Cell"

class FTChooseTracked: UIViewController {

    var viewModel = ViewModel()
    let items = ["Hello there", "my people"]
    
    var category: String = ""
    var numEx: Int = 1
    
    @IBOutlet weak var instructions: UILabel!
    @IBOutlet weak var tableView: UITableView?
    @IBOutlet weak var nextButton: UIButton?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        let vmitems = self.items.map { ViewModelItem(item: Model(title: $0)) }
        self.viewModel.setItems(items: vmitems)
        instructions.text = "Choose at most \(numEx) tracked exercises"
        
        tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
        tableView?.estimatedRowHeight = 100
        tableView?.rowHeight = UITableViewAutomaticDimension
        tableView?.allowsMultipleSelection = true
        tableView?.dataSource = viewModel
        tableView?.delegate = viewModel
        tableView?.separatorStyle = .none
        
        viewModel.didToggleSelection = { [weak self] hasSelection in
            self?.nextButton?.isEnabled = hasSelection
        }
    }
    
    @IBAction func next(_ sender: Any) {
        print(viewModel.selectedItems.map { $0.title })
        tableView?.reloadData()
    }
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
