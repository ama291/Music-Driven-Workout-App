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
    
    var userID: String = "1"
    var category: String = ""
    var numEx: Int = 1
    var reply: [[String:Any]] = [[String:Any]]()
    var exList: [String] = [String]()
    
    @IBOutlet weak var instructions: UILabel!
    @IBOutlet weak var tableView: UITableView?
    @IBOutlet weak var nextButton: UIButton?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        instructions.text = "Choose at most \(numEx) tracked exercises"

        let qstr = "userid=\(userID)&key=SoftCon2018"
        let request = APIRequest()
        
        request.submitPostLocal(route: "/api/fitness/tracked/", qstring: qstr) { (data, response, error) -> Void in
            if let error = error {
                fatalError(error.localizedDescription)
            }
//            self.reply = request.parseJsonRespone(data: data!)!
            self.reply = [["name": "Push ups", "id": 1], ["name": "chin ups", "id": 2]]
            //            names = reply.map { $0["name"] }
            for rep in self.reply {
                self.exList.append(rep["name"]! as! String)
            }
            let vmitems = self.exList.map { ViewModelItem(item: Model(title: $0)) }
            self.viewModel.setItems(items: vmitems)
            
            
            DispatchQueue.main.async {
                self.tableView?.register(CustomCell.nib, forCellReuseIdentifier: CustomCell.identifier)
                self.tableView?.dataSource = self.viewModel
                self.tableView?.delegate = self.viewModel
                self.tableView?.estimatedRowHeight = 100
                self.tableView?.rowHeight = UITableViewAutomaticDimension
                self.tableView?.allowsMultipleSelection = true
                self.tableView?.separatorStyle = .none
            }
            
            }.resume()
        

        
        
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
